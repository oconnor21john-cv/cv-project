# Effectiveness Report

Generated: 2026-03-09T22:24:57
Ground truth: manual annotations

## Core Metrics

- Query success rate: 1.000
- Recipes/query (mean): 11.38
- Source diversity/query (mean): 6.00
- Latency p50/p95: 42141 / 43886 ms
- Completeness mean: 1.000
- Artifact-free rate: 1.000
- Allergen macro precision/recall/F1: 0.569 / 0.730 / 0.642
- Allergen overall FNR: 0.209
- Uncertain labels excluded from allergen metrics: 45

## Source Summary

| source             |   trials |   success_rate |   success_ci_low |   success_ci_high |   availability_rate |   availability_ci_low |   availability_ci_high |   rate_403 |   source_unavailable_rate |   fallback_activation_rate |   fallback_ci_low |   fallback_ci_high |   recipes_mean |   recipes_median |   recipes_mean_ci_low |   recipes_mean_ci_high |   recipes_median_ci_low |   recipes_median_ci_high |   latency_p50_ms |   latency_p95_ms |   latency_median_ci_low |   latency_median_ci_high |
|:-------------------|---------:|---------------:|-----------------:|------------------:|--------------------:|----------------------:|-----------------------:|-----------:|--------------------------:|---------------------------:|------------------:|-------------------:|---------------:|-----------------:|----------------------:|-----------------------:|------------------------:|-------------------------:|-----------------:|-----------------:|------------------------:|-------------------------:|
| bbc                |        8 |              1 |         0.675592 |                 1 |                   1 |              0.675592 |                      1 |          0 |                         0 |                          0 |                 0 |           0.324408 |          2     |              2   |                 2     |                  2     |                       2 |                        2 |          6908.87 |          7483.39 |                 6137.3  |                  7372.52 |
| bbcgoodfood        |        8 |              1 |         0.675592 |                 1 |                   1 |              0.675592 |                      1 |          0 |                         0 |                          0 |                 0 |           0.324408 |          2     |              2   |                 2     |                  2     |                       2 |                        2 |          6747.82 |          6975.92 |                 6527.3  |                  6892.96 |
| foodafactoflife    |        8 |              1 |         0.675592 |                 1 |                   1 |              0.675592 |                      1 |          0 |                         0 |                          0 |                 0 |           0.324408 |          1.5   |              1.5 |                 1.125 |                  1.875 |                       1 |                        2 |          6066.52 |          7311.77 |                 5032.23 |                  6826.25 |
| ocado              |        8 |              1 |         0.675592 |                 1 |                   1 |              0.675592 |                      1 |          0 |                         0 |                          0 |                 0 |           0.324408 |          2     |              2   |                 2     |                  2     |                       2 |                        2 |          6942.79 |          7346.13 |                 6712.52 |                  7190.16 |
| realfooddietitians |        8 |              1 |         0.675592 |                 1 |                   1 |              0.675592 |                      1 |          0 |                         0 |                          0 |                 0 |           0.324408 |          2     |              2   |                 2     |                  2     |                       2 |                        2 |          7552.81 |          8936.36 |                 6831.78 |                  8911.34 |
| tomkerridge        |        8 |              1 |         0.675592 |                 1 |                   1 |              0.675592 |                      1 |          0 |                         0 |                          0 |                 0 |           0.324408 |          1.875 |              2   |                 1.625 |                  2     |                       2 |                        2 |          8055.7  |          8776.12 |                 7678.62 |                  8743.1  |

## Notes

- Safe filter effectiveness: proportion of retained recipes that were truly allergen-free.
- Confidence calibration: precision per HIGH/MEDIUM/LOW tier against ground truth.