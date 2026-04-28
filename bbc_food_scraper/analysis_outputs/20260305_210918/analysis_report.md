# Statistical Analysis Report

Generated: 2026-03-05T21:14:36

## Descriptive Summary by Source

| source   |   trials |   success_rate |   success_rate_ci_low |   success_rate_ci_high |   rate_403 |   source_unavailable_rate |   fallback_activation_rate |   fallback_ci_low |   fallback_ci_high |   recipes_mean |   recipes_median |   recipes_mean_ci_low |   recipes_mean_ci_high |   recipes_median_ci_low |   recipes_median_ci_high |   latency_p50_ms |   latency_p95_ms |   latency_median_ci_low |   latency_median_ci_high |   completeness_mean |   completeness_median |   completeness_mean_ci_low |   completeness_mean_ci_high |   availability_rate |   availability_ci_low |   availability_ci_high |
|:---------|---------:|---------------:|----------------------:|-----------------------:|-----------:|--------------------------:|---------------------------:|------------------:|-------------------:|---------------:|-----------------:|----------------------:|-----------------------:|------------------------:|-------------------------:|-----------------:|-----------------:|------------------------:|-------------------------:|--------------------:|----------------------:|---------------------------:|----------------------------:|--------------------:|----------------------:|-----------------------:|
| bbc      |      100 |              1 |              0.963007 |                      1 |          0 |                         0 |                          0 |                 0 |          0.0369935 |              1 |                1 |                     1 |                      1 |                       1 |                        1 |          2386.18 |          3121.74 |                 2250.01 |                  2550.46 |                   1 |                     1 |                          1 |                           1 |                   1 |              0.963007 |                      1 |

## Hypothesis Tests

No inferential tests were applicable for the active source set.

## Output Files

- `trial_results.csv`
- `recipe_quality.csv`
- `formatting_paired.csv`
- `source_descriptive_summary.csv`
- `pairwise_mannwhitney.csv` (if available)
- `hypothesis_tests.csv`
- `formatting_quality_summary.csv` (if recipe rows available)
- `boxplot_recipes_per_query.png`
- `boxplot_latency_ms.png`
- `bar_rates_by_source.png`

## Notes

- Allergen precision/recall is not computed automatically here because it requires a manually labeled ground-truth subset.
- To evaluate allergen detection, add a labeled CSV of true allergen presence and compute precision/recall/F1 with bootstrap CIs.