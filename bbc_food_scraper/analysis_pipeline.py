import argparse
import json
import os
import random
import re
import time
from collections import defaultdict
from datetime import datetime
from itertools import combinations
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy import stats
from scraper import MultiSourceScraper
from statsmodels.stats.contingency_tables import Table2x2, mcnemar
from statsmodels.stats.multitest import multipletests
from statsmodels.stats.proportion import proportion_confint


DEFAULT_QUERIES = [
    ("chicken curry", "main"),
    ("vegetarian pasta", "main"),
    ("chocolate cake", "dessert"),
    ("beef stew", "main"),
    ("mushroom soup", "main"),
    ("salmon", "main"),
    ("lentil dal", "main"),
    ("apple pie", "dessert"),
    ("lasagne", "main"),
    ("thai curry", "main"),
    ("brownies", "dessert"),
    ("risotto", "main"),
    ("vegan burger", "main"),
    ("banana bread", "dessert"),
    ("roast chicken", "main"),
    ("tacos", "main"),
    ("pancakes", "breakfast"),
    ("omelette", "breakfast"),
    ("ramen", "main"),
    ("stir fry", "main"),
]

def wilson_ci(k: int, n: int, alpha: float = 0.05):
    if n == 0:
        return (np.nan, np.nan)
    low, high = proportion_confint(k, n, alpha=alpha, method="wilson")
    return float(low), float(high)


def bootstrap_ci(values, stat="mean", n_boot=3000, alpha=0.05, seed=42):
    vals = np.array([v for v in values if pd.notna(v)], dtype=float)
    if len(vals) == 0:
        return (np.nan, np.nan)
    if len(vals) == 1:
        return (float(vals[0]), float(vals[0]))

    rng = np.random.default_rng(seed)
    boot_stats = []
    for _ in range(n_boot):
        sample = rng.choice(vals, size=len(vals), replace=True)
        if stat == "median":
            boot_stats.append(np.median(sample))
        else:
            boot_stats.append(np.mean(sample))

    lower = np.quantile(boot_stats, alpha / 2)
    upper = np.quantile(boot_stats, 1 - alpha / 2)
    return float(lower), float(upper)


def has_formatting_artifact(text: str) -> bool:
    if not text:
        return False
    return bool(
        re.search(r"https?://\S+", text)
        or re.search(r"!\[[^\]]*\]\([^)]+\)", text)
        or re.search(r"\[[^\]]+\]\([^)]+\)", text)
    )


def recipe_completeness(recipe: dict) -> float:
    required_fields = ["title", "url", "source", "ingredients", "instructions"]
    present = 0
    for field in required_fields:
        value = recipe.get(field)
        if field in ("ingredients", "instructions"):
            if isinstance(value, list) and len(value) > 0:
                present += 1
        elif value:
            present += 1
    return present / len(required_fields)


def old_style_raw_step_has_artifact(markdown: str) -> bool:
    """Simulate pre-cleanup parsing to build paired before/after artifact data."""
    if not markdown:
        return False

    lines = [line.strip() for line in markdown.splitlines() if line.strip()]
    start_idx = 0
    for i, line in enumerate(lines):
        if line.lower() == "keep screen awake":
            start_idx = i + 1
            break

    first_step_idx = None
    for i in range(start_idx, len(lines)):
        if re.match(r"^\d+\.\s+", lines[i]):
            first_step_idx = i
            break

    if first_step_idx is None:
        return False

    current_step = ""
    steps = []
    for line in lines[first_step_idx:]:
        step_match = re.match(r"^\d+\.\s+(.*)$", line)
        if step_match:
            if current_step:
                steps.append(current_step.strip())
            current_step = step_match.group(1).strip()
            continue
        if current_step:
            if line.startswith("|") or line.startswith("Nutrition") or line.startswith("©"):
                break
            if line.startswith("**Love the recipe"):
                break
            current_step += f" {line}"
    if current_step:
        steps.append(current_step.strip())

    joined = " ".join(steps)
    return has_formatting_artifact(joined)


def run_trials(
    output_dir: Path,
    repeats: int,
    max_results: int,
    seed: int,
    queries: list,
    compute_prepost: bool,
    fast_mode: bool,
):
    random.seed(seed)
    np.random.seed(seed)

    scraper = MultiSourceScraper()
    active_sources = sorted(scraper.scrapers.keys())
    trials = []
    recipes_rows = []
    paired_rows = []
    run_idx = 0

    for repeat in range(repeats):
        for query, category in queries:
            for source in active_sources:
                run_idx += 1
                started = time.perf_counter()
                source_scraper = scraper.scrapers[source]
                if fast_mode and not source_scraper.fast_mode:
                    source_scraper.fast_mode = True
                recipes = source_scraper.search_recipes(query=query, max_results=max_results)
                elapsed_ms = (time.perf_counter() - started) * 1000.0

                source_status = scraper._build_source_status(source, source_scraper, len(recipes))
                http_statuses = source_status.get("http_statuses", [])
                fallbacks = source_status.get("fallbacks_used", {})
                source_label = source_status.get("name", source)
                status = source_status.get("status", "unknown")
                recipes_found = len(recipes)
                success = int(recipes_found > 0)

                row = {
                    "run_idx": run_idx,
                    "repeat": repeat + 1,
                    "query": query,
                    "query_category": category,
                    "source": source,
                    "source_name": source_label,
                    "source_status": status,
                    "recipes_found": recipes_found,
                    "success": success,
                    "has_403": int(403 in http_statuses),
                    "latency_ms": elapsed_ms,
                    "fallback_external_used": int(fallbacks.get("external_search", False)),
                    "fallback_mirror_used": int(fallbacks.get("mirror", False)),
                    "source_unavailable": int(
                        status in ("temporarily_unavailable", "unavailable", "error")
                    ),
                    "http_statuses": json.dumps(http_statuses),
                }
                trials.append(row)
                pd.DataFrame(trials).to_csv(output_dir / "trial_results_partial.csv", index=False)

                for recipe in recipes:
                    instr_text = " ".join(recipe.get("instructions", []) or [])
                    ing_text = " ".join(recipe.get("ingredients", []) or [])
                    artifact = int(
                        has_formatting_artifact(instr_text) or has_formatting_artifact(ing_text)
                    )
                    completeness = recipe_completeness(recipe)

                    recipe_row = {
                        "run_idx": run_idx,
                        "repeat": repeat + 1,
                        "query": query,
                        "query_category": category,
                        "source": source,
                        "source_name": source_label,
                        "recipe_title": recipe.get("title", ""),
                        "recipe_url": recipe.get("url", ""),
                        "extraction_method": recipe.get("extraction_method", ""),
                        "has_title": int(bool(recipe.get("title"))),
                        "has_ingredients": int(bool(recipe.get("ingredients"))),
                        "has_instructions": int(bool(recipe.get("instructions"))),
                        "has_image": int(bool(recipe.get("image"))),
                        "ingredient_count": len(recipe.get("ingredients", []) or []),
                        "instruction_count": len(recipe.get("instructions", []) or []),
                        "completeness_score": completeness,
                        "formatting_artifact": artifact,
                    }
                    recipes_rows.append(recipe_row)
                    pd.DataFrame(recipes_rows).to_csv(
                        output_dir / "recipe_quality_partial.csv", index=False
                    )

                    # Build paired pre/post quality label for mirror-extracted recipes.
                    if compute_prepost and recipe.get("extraction_method") == "Mirror markdown parsing":
                        mirror_md = scraper.scrapers[source]._fetch_markdown_via_mirror(
                            recipe.get("url", "")
                        )
                        raw_has_artifact = int(old_style_raw_step_has_artifact(mirror_md or ""))
                        cleaned_has_artifact = artifact
                        paired_rows.append(
                            {
                                "source": source,
                                "query": query,
                                "recipe_url": recipe.get("url", ""),
                                "raw_has_artifact": raw_has_artifact,
                                "cleaned_has_artifact": cleaned_has_artifact,
                            }
                        )
                        pd.DataFrame(paired_rows).to_csv(
                            output_dir / "formatting_paired_partial.csv", index=False
                        )

                print(
                    f"[ANALYSIS] run {run_idx}: {query} | {source} | "
                    f"recipes={recipes_found} status={status} latency={elapsed_ms:.0f}ms"
                , flush=True)

    trials_df = pd.DataFrame(trials)
    recipes_df = pd.DataFrame(recipes_rows)
    paired_df = pd.DataFrame(paired_rows)

    trials_df.to_csv(output_dir / "trial_results.csv", index=False)
    recipes_df.to_csv(output_dir / "recipe_quality.csv", index=False)
    paired_df.to_csv(output_dir / "formatting_paired.csv", index=False)
    return trials_df, recipes_df, paired_df


def build_source_summary_df(trials_df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute per-source descriptive statistics from a trials dataframe.
    Shared by both analysis_pipeline and effectiveness_evaluation to avoid duplication.
    Expects columns: source, success, has_403, source_unavailable,
    fallback_external_used, fallback_mirror_used, recipes_found, latency_ms.
    """
    rows = []
    for source, group in trials_df.groupby("source"):
        n = len(group)
        succ = int(group["success"].sum())
        unavailable = int(group["source_unavailable"].sum())
        has403 = int(group["has_403"].sum())
        fallback = int((group.get("fallback_external_used", pd.Series(0, index=group.index)) |
                        group.get("fallback_mirror_used", pd.Series(0, index=group.index))).sum())
        counts = group["recipes_found"].tolist()
        lat = group["latency_ms"].tolist()

        succ_ci = wilson_ci(succ, n)
        avail_ci = wilson_ci(n - unavailable, n)
        fallback_ci = wilson_ci(fallback, n)

        rows.append({
            "source": source,
            "trials": n,
            "success_rate": succ / n if n else np.nan,
            "success_ci_low": succ_ci[0],
            "success_ci_high": succ_ci[1],
            "availability_rate": (n - unavailable) / n if n else np.nan,
            "availability_ci_low": avail_ci[0],
            "availability_ci_high": avail_ci[1],
            "rate_403": has403 / n if n else np.nan,
            "source_unavailable_rate": unavailable / n if n else np.nan,
            "fallback_activation_rate": fallback / n if n else np.nan,
            "fallback_ci_low": fallback_ci[0],
            "fallback_ci_high": fallback_ci[1],
            "recipes_mean": float(np.mean(counts)) if counts else np.nan,
            "recipes_median": float(np.median(counts)) if counts else np.nan,
            "recipes_mean_ci_low": bootstrap_ci(counts, "mean")[0],
            "recipes_mean_ci_high": bootstrap_ci(counts, "mean")[1],
            "recipes_median_ci_low": bootstrap_ci(counts, "median")[0],
            "recipes_median_ci_high": bootstrap_ci(counts, "median")[1],
            "latency_p50_ms": float(np.percentile(lat, 50)) if lat else np.nan,
            "latency_p95_ms": float(np.percentile(lat, 95)) if lat else np.nan,
            "latency_median_ci_low": bootstrap_ci(lat, "median")[0],
            "latency_median_ci_high": bootstrap_ci(lat, "median")[1],
        })
    return pd.DataFrame(rows)


def run_stats(output_dir: Path, trials_df: pd.DataFrame, recipes_df: pd.DataFrame, paired_df: pd.DataFrame):
    stats_payload = {}
    active_sources = sorted(trials_df["source"].dropna().unique().tolist())

    # Trial-level completeness proxy (mean of recipe completeness per run).
    if not recipes_df.empty:
        trial_comp = (
            recipes_df.groupby("run_idx")["completeness_score"].mean().reset_index()
        )
        trials_df = trials_df.merge(trial_comp, on="run_idx", how="left")
    else:
        trials_df["completeness_score"] = np.nan

    summary_df = build_source_summary_df(trials_df)

    # Append completeness columns (pipeline-specific).
    comp_rows = []
    for source, group in trials_df.groupby("source"):
        comp = [v for v in group["completeness_score"].tolist() if pd.notna(v)]
        comp_rows.append({
            "source": source,
            "completeness_mean": float(np.mean(comp)) if comp else np.nan,
            "completeness_median": float(np.median(comp)) if comp else np.nan,
            "completeness_mean_ci_low": bootstrap_ci(comp, "mean")[0] if comp else np.nan,
            "completeness_mean_ci_high": bootstrap_ci(comp, "mean")[1] if comp else np.nan,
        })
    summary_df = summary_df.merge(pd.DataFrame(comp_rows), on="source", how="left")
    summary_df.to_csv(output_dir / "source_descriptive_summary.csv", index=False)

    # Non-parametric group comparisons across sources.
    test_results = []
    pairwise_rows = []
    for metric in ["recipes_found", "latency_ms", "completeness_score"]:
        grouped = [
            g[metric].dropna().values for _, g in trials_df.groupby("source")
            if len(g[metric].dropna()) > 0
        ]
        all_vals = np.concatenate(grouped) if grouped else np.array([])
        if len(grouped) >= 2 and len(all_vals) > 0 and np.nanstd(all_vals) > 0:
            kw = stats.kruskal(*grouped, nan_policy="omit")
            test_results.append(
                {"test": "kruskal_wallis", "metric": metric, "statistic": kw.statistic, "p_value": kw.pvalue}
            )

            temp_pairs = []
            for a, b in combinations(active_sources, 2):
                va = trials_df.loc[trials_df["source"] == a, metric].dropna().values
                vb = trials_df.loc[trials_df["source"] == b, metric].dropna().values
                if len(va) > 0 and len(vb) > 0:
                    if np.nanstd(np.concatenate([va, vb])) == 0:
                        continue
                    u = stats.mannwhitneyu(va, vb, alternative="two-sided")
                    rank_biserial = 1 - (2 * u.statistic) / (len(va) * len(vb))
                    temp_pairs.append(
                        {
                            "metric": metric,
                            "source_a": a,
                            "source_b": b,
                            "u_statistic": u.statistic,
                            "p_value": u.pvalue,
                            "rank_biserial": rank_biserial,
                        }
                    )
            if temp_pairs:
                pvals = [r["p_value"] for r in temp_pairs]
                _, p_adj, _, _ = multipletests(pvals, method="fdr_bh")
                for idx, r in enumerate(temp_pairs):
                    r["p_value_bh"] = p_adj[idx]
                    pairwise_rows.append(r)

    # Binary outcomes: success/failure by source.
    contingency = pd.crosstab(trials_df["source"], trials_df["success"])
    if contingency.shape[1] == 2 and contingency.shape[0] >= 2:
        chi2, p, dof, _ = stats.chi2_contingency(contingency.values)
        test_results.append(
            {
                "test": "chi_square_success_by_source",
                "metric": "success",
                "statistic": chi2,
                "p_value": p,
                "dof": dof,
            }
        )

        # Pairwise odds ratios.
        or_rows = []
        for a, b in combinations(active_sources, 2):
            a_s = int(((trials_df["source"] == a) & (trials_df["success"] == 1)).sum())
            a_f = int(((trials_df["source"] == a) & (trials_df["success"] == 0)).sum())
            b_s = int(((trials_df["source"] == b) & (trials_df["success"] == 1)).sum())
            b_f = int(((trials_df["source"] == b) & (trials_df["success"] == 0)).sum())
            # Add continuity correction if needed.
            if 0 in [a_s, a_f, b_s, b_f]:
                table = np.array([[a_s + 0.5, a_f + 0.5], [b_s + 0.5, b_f + 0.5]])
            else:
                table = np.array([[a_s, a_f], [b_s, b_f]])
            ct = Table2x2(table)
            or_rows.append(
                {
                    "source_a": a,
                    "source_b": b,
                    "odds_ratio": ct.oddsratio,
                    "or_ci_low": ct.oddsratio_confint()[0],
                    "or_ci_high": ct.oddsratio_confint()[1],
                }
            )
        pd.DataFrame(or_rows).to_csv(output_dir / "pairwise_odds_ratios.csv", index=False)

    # Before/after formatting cleanup paired test (only with discordant pairs).
    if not paired_df.empty:
        # McNemar requires 2x2 paired disagreement matrix.
        b = int(((paired_df["raw_has_artifact"] == 1) & (paired_df["cleaned_has_artifact"] == 0)).sum())
        c = int(((paired_df["raw_has_artifact"] == 0) & (paired_df["cleaned_has_artifact"] == 1)).sum())
        a = int(((paired_df["raw_has_artifact"] == 0) & (paired_df["cleaned_has_artifact"] == 0)).sum())
        d = int(((paired_df["raw_has_artifact"] == 1) & (paired_df["cleaned_has_artifact"] == 1)).sum())
        table = np.array([[a, b], [c, d]])
        if (b + c) > 0:
            mcn = mcnemar(table, exact=True)
            test_results.append(
                {
                    "test": "mcnemar_formatting_artifact_pre_post",
                    "metric": "artifact_binary",
                    "statistic": float(mcn.statistic),
                    "p_value": float(mcn.pvalue),
                    "n_pairs": len(paired_df),
                    "improved_pairs": b,
                    "regressed_pairs": c,
                }
            )

        # Wilcoxon on paired binary difference (acts as sign-rank on paired deltas).
        deltas = paired_df["raw_has_artifact"] - paired_df["cleaned_has_artifact"]
        if len(deltas.unique()) > 1 and (deltas != 0).any():
            w = stats.wilcoxon(deltas)
            test_results.append(
                {
                    "test": "wilcoxon_pre_post_binary_delta",
                    "metric": "artifact_delta",
                    "statistic": float(w.statistic),
                    "p_value": float(w.pvalue),
                }
            )

    # Removed logistic regression from default analysis because frequent perfect-separation
    # in sparse blocked-source conditions produced unstable/non-informative estimates.

    if pairwise_rows:
        pd.DataFrame(pairwise_rows).to_csv(output_dir / "pairwise_mannwhitney.csv", index=False)
    else:
        (output_dir / "pairwise_mannwhitney.csv").write_text(
            "metric,source_a,source_b,u_statistic,p_value,rank_biserial,p_value_bh\n",
            encoding="utf-8",
        )
    if test_results:
        pd.DataFrame(test_results).to_csv(output_dir / "hypothesis_tests.csv", index=False)
    else:
        (output_dir / "hypothesis_tests.csv").write_text(
            "test,metric,statistic,p_value,dof,n_pairs,improved_pairs,regressed_pairs,note\n",
            encoding="utf-8",
        )

    # Recipe-level formatting artefact stats.
    if not recipes_df.empty:
        fmt_rows = []
        for source, g in recipes_df.groupby("source"):
            n = len(g)
            good = int((g["formatting_artifact"] == 0).sum())
            ci_low, ci_high = wilson_ci(good, n)
            fmt_rows.append(
                {
                    "source": source,
                    "n_recipes": n,
                    "artifact_free_rate": good / n if n else np.nan,
                    "artifact_free_ci_low": ci_low,
                    "artifact_free_ci_high": ci_high,
                }
            )
        pd.DataFrame(fmt_rows).to_csv(output_dir / "formatting_quality_summary.csv", index=False)

    # Charts
    sns.set_theme(style="whitegrid")
    plt.figure(figsize=(10, 5))
    sns.boxplot(data=trials_df, x="source", y="recipes_found")
    plt.title("Recipes Returned per Query by Source")
    plt.tight_layout()
    plt.savefig(output_dir / "boxplot_recipes_per_query.png", dpi=160)
    plt.close()

    plt.figure(figsize=(10, 5))
    sns.boxplot(data=trials_df, x="source", y="latency_ms")
    plt.title("Latency Distribution by Source (ms)")
    plt.tight_layout()
    plt.savefig(output_dir / "boxplot_latency_ms.png", dpi=160)
    plt.close()

    rate_df = (
        trials_df.groupby("source")[["success", "has_403", "source_unavailable"]]
        .mean()
        .reset_index()
        .melt(id_vars="source", var_name="metric", value_name="rate")
    )
    plt.figure(figsize=(10, 5))
    sns.barplot(data=rate_df, x="source", y="rate", hue="metric")
    plt.ylim(0, 1)
    plt.title("Key Binary Rates by Source")
    plt.tight_layout()
    plt.savefig(output_dir / "bar_rates_by_source.png", dpi=160)
    plt.close()

    stats_payload["summary_rows"] = len(summary_df)
    with open(output_dir / "analysis_meta.json", "w", encoding="utf-8") as fh:
        json.dump(stats_payload, fh, indent=2)


def write_report(output_dir: Path):
    summary = pd.read_csv(output_dir / "source_descriptive_summary.csv")
    try:
        tests = pd.read_csv(output_dir / "hypothesis_tests.csv")
    except pd.errors.EmptyDataError:
        tests = pd.DataFrame(columns=["test", "metric", "statistic", "p_value", "note"])

    lines = []
    lines.append("# Analysis Report")
    lines.append("")
    lines.append(f"Generated: {datetime.now().isoformat(timespec='seconds')}")
    lines.append("")
    lines.append("## Descriptive Summary by Source")
    lines.append("")
    lines.append(summary.to_markdown(index=False))
    lines.append("")
    lines.append("## Hypothesis Tests")
    lines.append("")
    if tests.empty:
        lines.append("No inferential tests were applicable for the active source set.")
    else:
        lines.append(tests.to_markdown(index=False))
    lines.append("")
    lines.append("## Output Files")
    lines.append("")
    lines.extend(
        [
            "- `trial_results.csv`",
            "- `recipe_quality.csv`",
            "- `formatting_paired.csv`",
            "- `source_descriptive_summary.csv`",
            "- `pairwise_mannwhitney.csv` (if available)",
            "- `hypothesis_tests.csv`",
            "- `formatting_quality_summary.csv` (if recipe rows available)",
            "- `boxplot_recipes_per_query.png`",
            "- `boxplot_latency_ms.png`",
            "- `bar_rates_by_source.png`",
        ]
    )
    lines.append("")
    lines.append("## Notes")
    lines.append("")
    lines.append(
        "- Allergen precision/recall requires a manually labelled ground-truth set — not computed here."
    )
    lines.append(
        "- To evaluate allergen detection, provide a labelled CSV and run precision/recall/F1 with bootstrap CIs."
    )

    (output_dir / "analysis_report.md").write_text("\n".join(lines), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Scraper analysis pipeline.")
    parser.add_argument("--repeats", type=int, default=1, help="Runs per query per source.")
    parser.add_argument("--max-results", type=int, default=3, help="Max results requested per trial.")
    parser.add_argument("--seed", type=int, default=42, help="Random seed.")
    parser.add_argument(
        "--output-dir",
        type=str,
        default=f"analysis_outputs/{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        help="Directory for outputs.",
    )
    parser.add_argument(
        "--query-limit",
        type=int,
        default=20,
        help="Number of default queries to include (max 20).",
    )
    parser.add_argument(
        "--compute-prepost",
        action="store_true",
        help="Compute paired pre/post formatting artifacts (adds extra mirror fetches).",
    )
    parser.add_argument(
        "--fast-mode",
        action="store_true",
        help="Speed up benchmarking by reducing retries and skipping external-search fallback.",
    )
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    query_limit = max(1, min(args.query_limit, len(DEFAULT_QUERIES)))
    queries = DEFAULT_QUERIES[:query_limit]

    print(f"[ANALYSIS] Output dir: {output_dir}")
    print(f"[ANALYSIS] Query count: {len(queries)} | repeats: {args.repeats}", flush=True)
    trials_df, recipes_df, paired_df = run_trials(
        output_dir=output_dir,
        repeats=args.repeats,
        max_results=args.max_results,
        seed=args.seed,
        queries=queries,
        compute_prepost=args.compute_prepost,
        fast_mode=args.fast_mode,
    )
    run_stats(output_dir, trials_df, recipes_df, paired_df)
    write_report(output_dir)
    print("[ANALYSIS] Done.")


if __name__ == "__main__":
    main()
