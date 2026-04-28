import argparse
import json
import re
import time
import warnings
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional

import numpy as np
import pandas as pd

from allergen_detector import ALLERGEN_DATABASE, AllergenDetector
from analysis_pipeline import (
    DEFAULT_QUERIES,
    bootstrap_ci,
    build_source_summary_df,
    has_formatting_artifact,
    recipe_completeness,
    wilson_ci,
)
from scraper import MultiSourceScraper


# ---------------------------------------------------------------------------
# Ground-truth helpers
# ---------------------------------------------------------------------------

def load_manual_annotations(csv_path: str) -> Dict[str, Dict[str, str]]:
    """
    Load a manually annotated ground-truth CSV.

    Expected format — one row per recipe, one column per allergen:
        recipe_url, gluten, milk, eggs, ... (14 allergen columns)
    Accepted cell values: present / absent / uncertain (case-insensitive).
    Rows with an unknown recipe_url are ignored.
    Returns: {recipe_url: {allergen_key: "present"|"absent"|"uncertain"}}
    """
    df = pd.read_csv(csv_path, dtype=str).fillna("uncertain")
    df.columns = [c.strip().lower() for c in df.columns]

    if "recipe_url" not in df.columns:
        raise ValueError(f"Annotations CSV must have a 'recipe_url' column. Found: {list(df.columns)}")

    allergen_keys = set(ALLERGEN_DATABASE.keys())
    missing = allergen_keys - set(df.columns)
    if missing:
        warnings.warn(
            f"Annotations CSV is missing columns for: {sorted(missing)}. "
            "Those allergens will fall back to silver truth."
        )

    annotations: Dict[str, Dict[str, str]] = {}
    for _, row in df.iterrows():
        url = str(row["recipe_url"]).strip()
        if not url:
            continue
        labels = {}
        for key in allergen_keys:
            val = str(row.get(key, "uncertain")).strip().lower()
            if val not in ("present", "absent", "uncertain"):
                val = "uncertain"
            labels[key] = val
        annotations[url] = labels
    return annotations


def _silver_truth_allergen_presence(ingredients, allergen_key: str) -> bool:
    """
    Lexicon-based fallback for recipes not covered by manual annotations.
    NOTE: because this uses the same keyword list as the detector it is
    circular — metrics derived from it measure internal consistency, not
    real-world accuracy. Use manual annotations wherever possible.
    """
    from allergen_detector import NON_DAIRY_MILK_PHRASES

    if not ingredients:
        return False

    def _normalise(text: str) -> str:
        text = (text or "").lower().replace("\u2019", "'")
        text = re.sub(r"[\(\)\[\]\{\},;:/\\|]+", " ", text)
        return re.sub(r"\s+", " ", text).strip()

    def _boundary(keyword: str, text: str) -> bool:
        esc = re.escape(keyword.strip().lower()).replace(r"\ ", r"[\s\-]+")
        return bool(re.search(rf"(?<![a-z0-9]){esc}(?![a-z0-9])", text, re.IGNORECASE))

    keywords = ALLERGEN_DATABASE[allergen_key]["keywords"]
    for ingredient in ingredients:
        norm = _normalise(ingredient)
        if allergen_key == "milk":
            if any(p in norm for p in NON_DAIRY_MILK_PHRASES):
                continue
        if any(_boundary(kw, norm) for kw in keywords):
            return True
    return False


def _resolve_truth(
    url: str,
    allergen_key: str,
    ingredients: list,
    annotations: Optional[Dict[str, Dict[str, str]]],
) -> Optional[int]:
    """
    Return 1 (present), 0 (absent), or None (uncertain/unknown).
    Uses manual annotations when available, falls back to silver truth.
    """
    if annotations and url in annotations:
        label = annotations[url].get(allergen_key, "uncertain")
        if label == "present":
            return 1
        if label == "absent":
            return 0
        return None  # uncertain — exclude from metrics

    # Silver-truth fallback (circular — see docstring above)
    return int(_silver_truth_allergen_presence(ingredients, allergen_key))


# ---------------------------------------------------------------------------
# Metrics
# ---------------------------------------------------------------------------

def compute_binary_metrics(y_true, y_pred):
    y_true = np.array(y_true, dtype=int)
    y_pred = np.array(y_pred, dtype=int)
    tp = int(((y_true == 1) & (y_pred == 1)).sum())
    tn = int(((y_true == 0) & (y_pred == 0)).sum())
    fp = int(((y_true == 0) & (y_pred == 1)).sum())
    fn = int(((y_true == 1) & (y_pred == 0)).sum())

    precision = tp / (tp + fp) if (tp + fp) else np.nan
    recall = tp / (tp + fn) if (tp + fn) else np.nan
    f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) else np.nan
    accuracy = (tp + tn) / len(y_true) if len(y_true) else np.nan
    fnr = fn / (tp + fn) if (tp + fn) else np.nan
    fpr = fp / (fp + tn) if (fp + tn) else np.nan

    return {
        "tp": tp, "tn": tn, "fp": fp, "fn": fn,
        "precision": precision, "recall": recall, "f1": f1,
        "accuracy": accuracy,
        "false_negative_rate": fnr,
        "false_positive_rate": fpr,
    }


# ---------------------------------------------------------------------------
# Benchmark
# ---------------------------------------------------------------------------

def run_benchmark(
    output_dir: Path,
    query_limit: int,
    repeats: int,
    max_results_per_source: int,
    annotations: Optional[Dict[str, Dict[str, str]]] = None,
):
    scraper = MultiSourceScraper()
    detector = AllergenDetector()
    sources = sorted(scraper.scrapers.keys())
    queries = DEFAULT_QUERIES[:query_limit]

    using_manual = bool(annotations)
    ground_truth_label = "manual_annotations" if using_manual else "silver_truth_CIRCULAR"
    if not using_manual:
        warnings.warn(
            "No annotations CSV provided. Allergen metrics will use the silver-truth "
            "lexicon fallback, which is circular with the detector. Results will reflect "
            "internal consistency only, not real-world accuracy."
        )

    trial_rows = []
    recipe_rows = []
    query_rows = []
    calibration_rows = []
    run_idx = 0

    for repeat in range(repeats):
        for query, category in queries:
            q_started = time.perf_counter()
            query_recipes = []
            source_status = {}

            for source in sources:
                run_idx += 1
                source_scraper = scraper.scrapers[source]
                started = time.perf_counter()
                recipes = source_scraper.search_recipes(query=query, max_results=max_results_per_source)
                latency_ms = (time.perf_counter() - started) * 1000.0
                status = scraper._build_source_status(source, source_scraper, len(recipes))
                source_status[source] = status

                trial_rows.append({
                    "run_idx": run_idx,
                    "repeat": repeat + 1,
                    "query": query,
                    "query_category": category,
                    "source": source,
                    "source_name": status.get("name", source),
                    "source_status": status.get("status", "unknown"),
                    "recipes_found": len(recipes),
                    "success": int(len(recipes) > 0),
                    "latency_ms": latency_ms,
                    "has_403": int(403 in status.get("http_statuses", [])),
                    "has_429": int(429 in status.get("http_statuses", [])),
                    "source_unavailable": int(
                        status.get("status") in ("temporarily_unavailable", "unavailable", "error")
                    ),
                    "fallback_external_used": int(status.get("fallbacks_used", {}).get("external_search", False)),
                    "fallback_mirror_used": int(status.get("fallbacks_used", {}).get("mirror", False)),
                })

                for recipe in recipes:
                    url = recipe.get("url", "")
                    ingredients = recipe.get("ingredients", []) or []
                    allergens_detected = detector.detect_allergens(ingredients)
                    predicted_medium_plus = set(
                        a for a, info in allergens_detected.items()
                        if info.get("confidence", "LOW") in ("MEDIUM", "HIGH")
                    )

                    # Resolved ground truth per allergen (None = uncertain, excluded from metrics).
                    truth_labels = {
                        a: _resolve_truth(url, a, ingredients, annotations)
                        for a in ALLERGEN_DATABASE.keys()
                    }
                    # Store only the definite labels for CSV; uncertain stored as empty string.
                    truth_for_csv = {
                        a: ("present" if v == 1 else "absent" if v == 0 else "uncertain")
                        for a, v in truth_labels.items()
                    }

                    # Calibration rows — confidence tier vs ground truth.
                    for allergen_key, info in allergens_detected.items():
                        truth_val = truth_labels.get(allergen_key)
                        if truth_val is None:
                            continue  # skip uncertain labels
                        calibration_rows.append({
                            "source": source,
                            "query": query,
                            "allergen": allergen_key,
                            "confidence": info.get("confidence", "LOW"),
                            "ground_truth": truth_val,
                            "ground_truth_source": ground_truth_label,
                        })

                    ingredient_text = " ".join(ingredients)
                    instruction_text = " ".join(recipe.get("instructions", []) or [])

                    recipe_rows.append({
                        "run_idx": run_idx,
                        "repeat": repeat + 1,
                        "query": query,
                        "query_category": category,
                        "source": source,
                        "source_name": status.get("name", source),
                        "recipe_title": recipe.get("title", ""),
                        "recipe_url": url,
                        "extraction_method": recipe.get("extraction_method", ""),
                        "ingredient_count": len(ingredients),
                        "instruction_count": len(recipe.get("instructions", []) or []),
                        "completeness_score": recipe_completeness(recipe),
                        "formatting_artifact": int(
                            has_formatting_artifact(ingredient_text)
                            or has_formatting_artifact(instruction_text)
                        ),
                        "predicted_allergens_medium_plus": json.dumps(sorted(predicted_medium_plus)),
                        "ground_truth_allergens": json.dumps(truth_for_csv),
                        "ground_truth_source": ground_truth_label,
                    })
                    query_recipes.append(recipe)

            q_latency_ms = (time.perf_counter() - q_started) * 1000.0
            urls = [r.get("url", "") for r in query_recipes if r.get("url")]
            duplicate_rate = 1.0 - (len(set(urls)) / len(urls)) if urls else np.nan
            distinct_sources = len({r.get("source", "") for r in query_recipes if r.get("source")})

            query_rows.append({
                "repeat": repeat + 1,
                "query": query,
                "query_category": category,
                "latency_ms": q_latency_ms,
                "recipes_found_total": len(query_recipes),
                "query_success": int(len(query_recipes) > 0),
                "distinct_sources_returned": distinct_sources,
                "duplicate_rate": duplicate_rate,
                "source_status": json.dumps(source_status),
            })

            print(
                f"[EVAL] repeat={repeat + 1} query='{query}' recipes={len(query_recipes)} "
                f"sources_with_results={distinct_sources} latency={q_latency_ms:.0f}ms",
                flush=True,
            )

    trials_df = pd.DataFrame(trial_rows)
    recipes_df = pd.DataFrame(recipe_rows)
    queries_df = pd.DataFrame(query_rows)
    calibration_df = pd.DataFrame(calibration_rows)

    trials_df.to_csv(output_dir / "effectiveness_trial_results.csv", index=False)
    recipes_df.to_csv(output_dir / "effectiveness_recipe_results.csv", index=False)
    queries_df.to_csv(output_dir / "effectiveness_query_results.csv", index=False)
    calibration_df.to_csv(output_dir / "effectiveness_calibration_rows.csv", index=False)

    return trials_df, recipes_df, queries_df, calibration_df


# ---------------------------------------------------------------------------
# Summarise
# ---------------------------------------------------------------------------

def summarize_metrics(
    output_dir: Path,
    trials_df,
    recipes_df,
    queries_df,
    calibration_df,
    annotations: Optional[Dict[str, Dict[str, str]]] = None,
):
    using_manual = bool(annotations)
    ground_truth_label = "manual annotations" if using_manual else "silver truth (CIRCULAR — lexicon fallback)"
    metrics = {}

    # Retrieval metrics
    metrics["query_success_rate"] = float(queries_df["query_success"].mean()) if not queries_df.empty else np.nan
    metrics["recipes_per_query_mean"] = float(queries_df["recipes_found_total"].mean()) if not queries_df.empty else np.nan
    metrics["recipes_per_query_median"] = float(queries_df["recipes_found_total"].median()) if not queries_df.empty else np.nan
    metrics["source_diversity_mean"] = float(queries_df["distinct_sources_returned"].mean()) if not queries_df.empty else np.nan
    metrics["duplicate_rate_mean"] = float(queries_df["duplicate_rate"].dropna().mean()) if not queries_df.empty else np.nan
    metrics["latency_p50_ms"] = float(np.percentile(queries_df["latency_ms"], 50)) if not queries_df.empty else np.nan
    metrics["latency_p95_ms"] = float(np.percentile(queries_df["latency_ms"], 95)) if not queries_df.empty else np.nan
    metrics["latency_median_ci_low"], metrics["latency_median_ci_high"] = (
        bootstrap_ci(queries_df["latency_ms"].tolist(), stat="median")
        if not queries_df.empty else (np.nan, np.nan)
    )

    # Source reliability — shared function, no duplication.
    source_df = build_source_summary_df(trials_df)
    source_df.to_csv(output_dir / "effectiveness_source_summary.csv", index=False)

    # Extraction quality
    if not recipes_df.empty:
        metrics["completeness_mean"] = float(recipes_df["completeness_score"].mean())
        metrics["completeness_median"] = float(recipes_df["completeness_score"].median())
        metrics["artifact_free_rate"] = float((recipes_df["formatting_artifact"] == 0).mean())
        ci_low, ci_high = wilson_ci(int((recipes_df["formatting_artifact"] == 0).sum()), len(recipes_df))
        metrics["artifact_free_ci_low"] = ci_low
        metrics["artifact_free_ci_high"] = ci_high
    else:
        for k in ("completeness_mean", "completeness_median", "artifact_free_rate",
                  "artifact_free_ci_low", "artifact_free_ci_high"):
            metrics[k] = np.nan

    # Allergen detection metrics against resolved ground truth.
    # For each recipe×allergen pair we look up the truth label.
    # Uncertain / unannotated entries are excluded from the calculation.
    allergen_rows = []
    overall_true, overall_pred = [], []
    n_excluded = 0

    for allergen_key in ALLERGEN_DATABASE.keys():
        y_true, y_pred = [], []
        for _, row in recipes_df.iterrows():
            pred_set = set(json.loads(row["predicted_allergens_medium_plus"]))
            truth_dict = json.loads(row["ground_truth_allergens"])
            truth_label = truth_dict.get(allergen_key, "uncertain")
            if truth_label == "uncertain":
                n_excluded += 1
                continue
            y_pred.append(int(allergen_key in pred_set))
            y_true.append(1 if truth_label == "present" else 0)
        m = compute_binary_metrics(y_true, y_pred) if y_true else {}
        allergen_rows.append({"allergen": allergen_key, **m})
        overall_true.extend(y_true)
        overall_pred.extend(y_pred)

    allergen_df = pd.DataFrame(allergen_rows)
    allergen_df.to_csv(output_dir / "effectiveness_allergen_metrics.csv", index=False)
    metrics["allergen_n_excluded_uncertain"] = n_excluded

    macro_precision = float(allergen_df["precision"].dropna().mean()) if not allergen_df.empty else np.nan
    macro_recall = float(allergen_df["recall"].dropna().mean()) if not allergen_df.empty else np.nan
    macro_f1 = float(allergen_df["f1"].dropna().mean()) if not allergen_df.empty else np.nan
    overall_metrics = compute_binary_metrics(overall_true, overall_pred) if overall_true else {}
    metrics["allergen_macro_precision"] = macro_precision
    metrics["allergen_macro_recall"] = macro_recall
    metrics["allergen_macro_f1"] = macro_f1
    metrics["allergen_overall_false_negative_rate"] = overall_metrics.get("false_negative_rate", np.nan)
    metrics["allergen_overall_false_positive_rate"] = overall_metrics.get("false_positive_rate", np.nan)
    metrics["ground_truth_source"] = ground_truth_label

    # Safe filter effectiveness
    safe_filter_rows = []
    for allergen_key in ALLERGEN_DATABASE.keys():
        if recipes_df.empty:
            continue
        retained_truth_safe = []
        for _, row in recipes_df.iterrows():
            pred_set = set(json.loads(row["predicted_allergens_medium_plus"]))
            truth_dict = json.loads(row["ground_truth_allergens"])
            truth_label = truth_dict.get(allergen_key, "uncertain")
            if truth_label == "uncertain":
                continue
            if allergen_key not in pred_set:  # recipe was retained (passed the filter)
                retained_truth_safe.append(1 if truth_label == "absent" else 0)
        if retained_truth_safe:
            safe_rate = float(np.mean(retained_truth_safe))
            ci_low, ci_high = wilson_ci(int(sum(retained_truth_safe)), len(retained_truth_safe))
        else:
            safe_rate, ci_low, ci_high = np.nan, np.nan, np.nan
        safe_filter_rows.append({
            "allergen": allergen_key,
            "safe_filter_effectiveness": safe_rate,
            "unsafe_return_rate": 1.0 - safe_rate if not np.isnan(safe_rate) else np.nan,
            "safe_filter_ci_low": ci_low,
            "safe_filter_ci_high": ci_high,
            "retained_recipe_count": len(retained_truth_safe),
        })
    safe_filter_df = pd.DataFrame(safe_filter_rows)
    safe_filter_df.to_csv(output_dir / "effectiveness_safe_filter_metrics.csv", index=False)

    # Confidence calibration — precision per tier against ground truth.
    # Uncertain labels are already excluded from calibration_rows at collection time.
    if not calibration_df.empty:
        calibration_summary = (
            calibration_df.groupby("confidence")["ground_truth"]
            .agg(count="count", correct="sum")
            .reset_index()
        )
        calibration_summary["precision"] = calibration_summary["correct"] / calibration_summary["count"]
        calibration_summary["ground_truth_source"] = ground_truth_label
    else:
        calibration_summary = pd.DataFrame(
            columns=["confidence", "count", "correct", "precision", "ground_truth_source"]
        )
    calibration_summary.to_csv(output_dir / "effectiveness_confidence_calibration.csv", index=False)

    with open(output_dir / "effectiveness_summary_metrics.json", "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)

    # Report
    gt_warning = (
        "\n> **Warning:** allergen metrics used the circular silver-truth lexicon fallback.\n"
        "> Re-run with `--annotations-csv` to get independent ground-truth results.\n"
        if not using_manual else ""
    )
    report_lines = [
        "# Effectiveness Report",
        "",
        f"Generated: {datetime.now().isoformat(timespec='seconds')}",
        f"Ground truth: {ground_truth_label}",
        gt_warning,
        "## Core Metrics",
        "",
        f"- Query success rate: {metrics['query_success_rate']:.3f}",
        f"- Recipes/query (mean): {metrics['recipes_per_query_mean']:.2f}",
        f"- Source diversity/query (mean): {metrics['source_diversity_mean']:.2f}",
        f"- Latency p50/p95: {metrics['latency_p50_ms']:.0f} / {metrics['latency_p95_ms']:.0f} ms",
        f"- Completeness mean: {metrics['completeness_mean']:.3f}",
        f"- Artifact-free rate: {metrics['artifact_free_rate']:.3f}",
        f"- Allergen macro precision/recall/F1: "
        f"{metrics['allergen_macro_precision']:.3f} / {metrics['allergen_macro_recall']:.3f} / {metrics['allergen_macro_f1']:.3f}",
        f"- Allergen overall FNR: {metrics['allergen_overall_false_negative_rate']:.3f}",
        f"- Uncertain labels excluded from allergen metrics: {metrics['allergen_n_excluded_uncertain']}",
        "",
        "## Source Summary",
        "",
        source_df.to_markdown(index=False),
        "",
        "## Notes",
        "",
        "- Safe filter effectiveness: proportion of retained recipes that were truly allergen-free.",
        "- Confidence calibration: precision per HIGH/MEDIUM/LOW tier against ground truth.",
    ]
    (output_dir / "effectiveness_report.md").write_text("\n".join(report_lines), encoding="utf-8")

    return metrics, source_df, allergen_df, safe_filter_df, calibration_summary


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="End-to-end effectiveness evaluation.")
    parser.add_argument("--query-limit", type=int, default=8)
    parser.add_argument("--repeats", type=int, default=1)
    parser.add_argument("--max-results-per-source", type=int, default=2)
    parser.add_argument(
        "--output-dir",
        type=str,
        default=f"analysis_outputs/{datetime.now().strftime('%Y%m%d_%H%M%S')}_effectiveness",
    )
    parser.add_argument(
        "--annotations-csv",
        type=str,
        default=None,
        help=(
            "Path to manual annotation CSV (recipe_url + one column per allergen). "
            "If omitted, metrics fall back to the circular silver-truth lexicon."
        ),
    )
    args = parser.parse_args()

    annotations = None
    if args.annotations_csv:
        print(f"[EVAL] Loading manual annotations from: {args.annotations_csv}", flush=True)
        annotations = load_manual_annotations(args.annotations_csv)
        print(f"[EVAL] Loaded annotations for {len(annotations)} recipes.", flush=True)
    else:
        print(
            "[EVAL] WARNING: No --annotations-csv provided. "
            "Allergen metrics will use circular silver-truth fallback.",
            flush=True,
        )

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    print(f"[EVAL] Output directory: {output_dir}", flush=True)

    trials_df, recipes_df, queries_df, calibration_df = run_benchmark(
        output_dir=output_dir,
        query_limit=max(1, min(args.query_limit, len(DEFAULT_QUERIES))),
        repeats=max(1, args.repeats),
        max_results_per_source=max(1, args.max_results_per_source),
        annotations=annotations,
    )
    summarize_metrics(output_dir, trials_df, recipes_df, queries_df, calibration_df, annotations=annotations)
    print("[EVAL] Completed.", flush=True)


if __name__ == "__main__":
    main()
