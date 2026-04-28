# Effectiveness Report

Generated: 2026-03-09T21:34:57
Ground truth: silver truth (CIRCULAR — lexicon fallback)

> **Warning:** allergen metrics used the circular silver-truth lexicon fallback.
> Re-run with `--annotations-csv` to get independent ground-truth results.

## Core Metrics

- Query success rate: 1.000
- Recipes/query (mean): 11.38
- Source diversity/query (mean): 6.00
- Latency p50/p95: 42395 / 43904 ms
- Completeness mean: 1.000
- Artifact-free rate: 1.000
- Allergen macro precision/recall/F1: 0.974 / 1.000 / 0.985
- Allergen overall FNR: 0.000
- Uncertain labels excluded from allergen metrics: 0

## Source Summary

| source             |   trials |   success_rate |   success_ci_low |   success_ci_high |   availability_rate |   availability_ci_low |   availability_ci_high |   rate_403 |   source_unavailable_rate |   fallback_activation_rate |   fallback_ci_low |   fallback_ci_high |   recipes_mean |   recipes_median |   recipes_mean_ci_low |   recipes_mean_ci_high |   recipes_median_ci_low |   recipes_median_ci_high |   latency_p50_ms |   latency_p95_ms |   latency_median_ci_low |   latency_median_ci_high |
|:-------------------|---------:|---------------:|-----------------:|------------------:|--------------------:|----------------------:|-----------------------:|-----------:|--------------------------:|---------------------------:|------------------:|-------------------:|---------------:|-----------------:|----------------------:|-----------------------:|------------------------:|-------------------------:|-----------------:|-----------------:|------------------------:|-------------------------:|
| bbc                |        8 |              1 |         0.675592 |                 1 |                   1 |              0.675592 |                      1 |          0 |                         0 |                          0 |                 0 |           0.324408 |          2     |              2   |                 2     |                  2     |                       2 |                        2 |          6359.26 |          6726.44 |                 6066.07 |                  6613.42 |
| bbcgoodfood        |        8 |              1 |         0.675592 |                 1 |                   1 |              0.675592 |                      1 |          0 |                         0 |                          0 |                 0 |           0.324408 |          2     |              2   |                 2     |                  2     |                       2 |                        2 |          6477.62 |          7112.96 |                 5784.12 |                  7088.9  |
| foodafactoflife    |        8 |              1 |         0.675592 |                 1 |                   1 |              0.675592 |                      1 |          0 |                         0 |                          0 |                 0 |           0.324408 |          1.5   |              1.5 |                 1.125 |                  1.875 |                       1 |                        2 |          5774.42 |          7168.07 |                 4445.42 |                  7018.85 |
| ocado              |        8 |              1 |         0.675592 |                 1 |                   1 |              0.675592 |                      1 |          0 |                         0 |                          0 |                 0 |           0.324408 |          2     |              2   |                 2     |                  2     |                       2 |                        2 |          6776.29 |          7653.72 |                 6422.6  |                  7313.76 |
| realfooddietitians |        8 |              1 |         0.675592 |                 1 |                   1 |              0.675592 |                      1 |          0 |                         0 |                          0 |                 0 |           0.324408 |          2     |              2   |                 2     |                  2     |                       2 |                        2 |          7620.27 |          9067.67 |                 6730.11 |                  8829.02 |
| tomkerridge        |        8 |              1 |         0.675592 |                 1 |                   1 |              0.675592 |                      1 |          0 |                         0 |                          0 |                 0 |           0.324408 |          1.875 |              2   |                 1.625 |                  2     |                       2 |                        2 |          7798.33 |          8365.16 |                 7263.09 |                  8285.05 |

## Notes

- Safe filter effectiveness: proportion of retained recipes that were truly allergen-free.
- Confidence calibration: precision per HIGH/MEDIUM/LOW tier against ground truth.