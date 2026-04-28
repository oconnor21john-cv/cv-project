# Effectiveness Report

Generated: 2026-03-09T21:58:38
Ground truth: silver truth (CIRCULAR — lexicon fallback)

> **Warning:** allergen metrics used the circular silver-truth lexicon fallback.
> Re-run with `--annotations-csv` to get independent ground-truth results.

## Core Metrics

- Query success rate: 1.000
- Recipes/query (mean): 11.38
- Source diversity/query (mean): 6.00
- Latency p50/p95: 43157 / 45576 ms
- Completeness mean: 1.000
- Artifact-free rate: 1.000
- Allergen macro precision/recall/F1: 0.974 / 1.000 / 0.985
- Allergen overall FNR: 0.000
- Uncertain labels excluded from allergen metrics: 0

## Source Summary

| source             |   trials |   success_rate |   success_ci_low |   success_ci_high |   availability_rate |   availability_ci_low |   availability_ci_high |   rate_403 |   source_unavailable_rate |   fallback_activation_rate |   fallback_ci_low |   fallback_ci_high |   recipes_mean |   recipes_median |   recipes_mean_ci_low |   recipes_mean_ci_high |   recipes_median_ci_low |   recipes_median_ci_high |   latency_p50_ms |   latency_p95_ms |   latency_median_ci_low |   latency_median_ci_high |
|:-------------------|---------:|---------------:|-----------------:|------------------:|--------------------:|----------------------:|-----------------------:|-----------:|--------------------------:|---------------------------:|------------------:|-------------------:|---------------:|-----------------:|----------------------:|-----------------------:|------------------------:|-------------------------:|-----------------:|-----------------:|------------------------:|-------------------------:|
| bbc                |        8 |              1 |         0.675592 |                 1 |                   1 |              0.675592 |                      1 |          0 |                         0 |                          0 |                 0 |           0.324408 |          2     |              2   |                 2     |                  2     |                       2 |                        2 |          7044.67 |          8193.46 |                 6543.86 |                  7867.23 |
| bbcgoodfood        |        8 |              1 |         0.675592 |                 1 |                   1 |              0.675592 |                      1 |          0 |                         0 |                          0 |                 0 |           0.324408 |          2     |              2   |                 2     |                  2     |                       2 |                        2 |          6707.09 |          6994.21 |                 6065.24 |                  6944.8  |
| foodafactoflife    |        8 |              1 |         0.675592 |                 1 |                   1 |              0.675592 |                      1 |          0 |                         0 |                          0 |                 0 |           0.324408 |          1.5   |              1.5 |                 1.125 |                  1.875 |                       1 |                        2 |          5551.22 |          7264.46 |                 4882.6  |                  6498.72 |
| ocado              |        8 |              1 |         0.675592 |                 1 |                   1 |              0.675592 |                      1 |          0 |                         0 |                          0 |                 0 |           0.324408 |          2     |              2   |                 2     |                  2     |                       2 |                        2 |          6462.14 |          7062.53 |                 6216.06 |                  6576.43 |
| realfooddietitians |        8 |              1 |         0.675592 |                 1 |                   1 |              0.675592 |                      1 |          0 |                         0 |                          0 |                 0 |           0.324408 |          2     |              2   |                 2     |                  2     |                       2 |                        2 |          7777.69 |          9097.8  |                 6956.7  |                  8608.28 |
| tomkerridge        |        8 |              1 |         0.675592 |                 1 |                   1 |              0.675592 |                      1 |          0 |                         0 |                          0 |                 0 |           0.324408 |          1.875 |              2   |                 1.625 |                  2     |                       2 |                        2 |          8341.53 |          8646.6  |                 7866.37 |                  8645.02 |

## Notes

- Safe filter effectiveness: proportion of retained recipes that were truly allergen-free.
- Confidence calibration: precision per HIGH/MEDIUM/LOW tier against ground truth.