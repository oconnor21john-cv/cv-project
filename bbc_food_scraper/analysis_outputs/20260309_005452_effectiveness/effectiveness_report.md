# Effectiveness Evaluation Report

Generated: 2026-03-09T01:00:34

## Core Metrics

- Query success rate: 1.000
- Recipes/query (mean): 11.38
- Source diversity/query (mean): 6.00
- Latency p50/p95: 42384 / 45049 ms
- Completeness mean: 1.000
- Artifact-free rate: 1.000
- Allergen macro precision/recall/F1: 0.920 / 1.000 / 0.948
- Allergen overall false negative rate: 0.000

## Source Summary

| source             |   trials |   success_rate |   success_ci_low |   success_ci_high |   source_unavailable_rate |   blocked_rate |   fallback_rate |   latency_p50_ms |   latency_p95_ms |   recipes_mean |
|:-------------------|---------:|---------------:|-----------------:|------------------:|--------------------------:|---------------:|----------------:|-----------------:|-----------------:|---------------:|
| bbc                |        8 |              1 |         0.675592 |                 1 |                         0 |              0 |               0 |          7160.29 |          7793.68 |          2     |
| bbcgoodfood        |        8 |              1 |         0.675592 |                 1 |                         0 |              0 |               0 |          7008.96 |          8097.27 |          2     |
| foodafactoflife    |        8 |              1 |         0.675592 |                 1 |                         0 |              0 |               0 |          5945.11 |          7826.34 |          1.5   |
| ocado              |        8 |              1 |         0.675592 |                 1 |                         0 |              0 |               0 |          6136.97 |          7293.66 |          2     |
| realfooddietitians |        8 |              1 |         0.675592 |                 1 |                         0 |              0 |               0 |          8570.23 |          9871.12 |          2     |
| tomkerridge        |        8 |              1 |         0.675592 |                 1 |                         0 |              0 |               0 |          7298.26 |          8106.68 |          1.875 |

## Notes

- Allergen accuracy uses a conservative lexicon-based silver-truth baseline derived from ingredient text.
- This is suitable for comparative benchmarking but does not replace expert human-labeled clinical validation.