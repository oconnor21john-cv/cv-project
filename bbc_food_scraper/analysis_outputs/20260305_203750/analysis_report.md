# Statistical Analysis Report

Generated: 2026-03-05T20:54:12

## Descriptive Summary by Source

| source   |   trials |   success_rate |   success_rate_ci_low |   success_rate_ci_high |   rate_403 |   source_unavailable_rate |   fallback_activation_rate |   fallback_ci_low |   fallback_ci_high |   recipes_mean |   recipes_median |   recipes_mean_ci_low |   recipes_mean_ci_high |   recipes_median_ci_low |   recipes_median_ci_high |   latency_p50_ms |   latency_p95_ms |   latency_median_ci_low |   latency_median_ci_high |   completeness_mean |   completeness_median |   completeness_mean_ci_low |   completeness_mean_ci_high |   availability_rate |   availability_ci_low |   availability_ci_high |
|:---------|---------:|---------------:|----------------------:|-----------------------:|-----------:|--------------------------:|---------------------------:|------------------:|-------------------:|---------------:|-----------------:|----------------------:|-----------------------:|------------------------:|-------------------------:|-----------------:|-----------------:|------------------------:|-------------------------:|--------------------:|----------------------:|---------------------------:|----------------------------:|--------------------:|----------------------:|-----------------------:|
| bbc      |        3 |       1        |              0.438503 |               1        |          0 |                  0        |                          0 |          0        |           0.561497 |       1        |                1 |                     1 |                      1 |                       1 |                        1 |          11969.1 |          12093.9 |                 11163.2 |                  12107.7 |                   1 |                     1 |                          1 |                           1 |            1        |              0.438503 |               1        |
| serious  |        3 |       0.666667 |              0.20766  |               0.938508 |          1 |                  0.333333 |                          1 |          0.438503 |           1        |       0.666667 |                1 |                     0 |                      1 |                       0 |                        1 |         181946   |         187645   |                150231   |                 188278   |                   1 |                     1 |                          1 |                           1 |            0.666667 |              0.20766  |               0.938508 |
| simply   |        3 |       0.666667 |              0.20766  |               0.938508 |          1 |                  0.333333 |                          1 |          0.438503 |           1        |       0.666667 |                1 |                     0 |                      1 |                       0 |                        1 |         152265   |         174559   |                 14908.2 |                 177036   |                   1 |                     1 |                          1 |                           1 |            0.666667 |              0.20766  |               0.938508 |

## Hypothesis Tests

| test                                 | metric             |   statistic |     p_value |   dof |   n_pairs |   improved_pairs |   regressed_pairs | note                           |
|:-------------------------------------|:-------------------|------------:|------------:|------:|----------:|-----------------:|------------------:|:-------------------------------|
| kruskal_wallis                       | recipes_found      |     1.14286 |   0.564718  |   nan |       nan |              nan |               nan | nan                            |
| kruskal_wallis                       | latency_ms         |     5.95556 |   0.0509058 |   nan |       nan |              nan |               nan | nan                            |
| kruskal_wallis                       | completeness_score |   nan       | nan         |   nan |       nan |              nan |               nan | nan                            |
| chi_square_success_by_source         | success            |     1.28571 |   0.525788  |     2 |       nan |              nan |               nan | nan                            |
| mcnemar_formatting_artifact_pre_post | artifact_binary    |     0       |   0.5       |   nan |         4 |                2 |                 0 | nan                            |
| wilcoxon_pre_post_binary_delta       | artifact_delta     |     0       |   0.5       |   nan |       nan |              nan |               nan | nan                            |
| logistic_regression                  | success            |   nan       | nan         |   nan |       nan |              nan |               nan | Model failed: math range error |

## Output Files

- `trial_results.csv`
- `recipe_quality.csv`
- `formatting_paired.csv`
- `source_descriptive_summary.csv`
- `pairwise_mannwhitney.csv` (if available)
- `pairwise_odds_ratios.csv` (if available)
- `logistic_success_model.csv` (if model converges)
- `hypothesis_tests.csv`
- `formatting_quality_summary.csv` (if recipe rows available)
- `boxplot_recipes_per_query.png`
- `boxplot_latency_ms.png`
- `bar_rates_by_source.png`

## Notes

- Allergen precision/recall is not computed automatically here because it requires a manually labeled ground-truth subset.
- To evaluate allergen detection, add a labeled CSV of true allergen presence and compute precision/recall/F1 with bootstrap CIs.