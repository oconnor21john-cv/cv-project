"""
generate_annotation_stubs.py

Run this after effectiveness_evaluation.py to produce a pre-populated
annotations CSV with all scraped recipe URLs already filled in.
Every allergen cell defaults to 'uncertain' — replace each with
'present' or 'absent' as you review the recipe.

Usage:
    python generate_annotation_stubs.py \
        --results-csv analysis_outputs/<run>/effectiveness_recipe_results.csv \
        --out annotations.csv

Then pass the completed file to the evaluation:
    python effectiveness_evaluation.py \
        --annotations-csv annotations.csv \
        --output-dir analysis_outputs/<run>_with_annotations
"""

import argparse
import csv
from pathlib import Path

import pandas as pd

ALLERGEN_KEYS = [
    'celery', 'gluten', 'crustaceans', 'eggs', 'fish', 'lupin',
    'milk', 'molluscs', 'mustard', 'nuts', 'peanuts', 'sesame',
    'soya', 'sulphites',
]


def generate_stubs(results_csv: str, out_path: str, dedupe: bool = True):
    df = pd.read_csv(results_csv, dtype=str)

    if 'recipe_url' not in df.columns:
        raise ValueError(
            f"Expected a 'recipe_url' column in {results_csv}. "
            f"Found: {list(df.columns)}"
        )

    urls = df['recipe_url'].dropna().str.strip()
    urls = urls[urls != '']

    if dedupe:
        urls = urls.drop_duplicates()

    rows = []
    for url in urls:
        row = {'recipe_url': url}
        # Include title and source as read-only helper columns so you know
        # which recipe you're looking at without opening every URL.
        recipe_rows = df[df['recipe_url'] == url].iloc[0]
        row['_title'] = recipe_rows.get('recipe_title', '')
        row['_source'] = recipe_rows.get('source_name', '')
        for key in ALLERGEN_KEYS:
            row[key] = 'uncertain'
        rows.append(row)

    fieldnames = ['recipe_url', '_title', '_source'] + ALLERGEN_KEYS
    out = Path(out_path)
    with open(out, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"[STUBS] Written {len(rows)} recipe stubs to {out}")
    print(f"[STUBS] Fill in each allergen column with: present / absent / uncertain")
    print(f"[STUBS] The _title and _source columns are for reference only and are ignored by the evaluator.")


def main():
    parser = argparse.ArgumentParser(description="Generate annotation stubs from a benchmark results CSV.")
    parser.add_argument(
        '--results-csv',
        required=True,
        help='Path to effectiveness_recipe_results.csv from a benchmark run.',
    )
    parser.add_argument(
        '--out',
        default='annotations.csv',
        help='Output path for the stub annotations CSV (default: annotations.csv).',
    )
    parser.add_argument(
        '--no-dedupe',
        action='store_true',
        help='Keep duplicate URLs (same recipe appearing in multiple query results).',
    )
    args = parser.parse_args()
    generate_stubs(args.results_csv, args.out, dedupe=not args.no_dedupe)


if __name__ == '__main__':
    main()
