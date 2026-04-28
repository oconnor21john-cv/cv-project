# Statistical Analysis Report

Generated: 2026-03-05T20:46:18

## Descriptive Summary by Source

| source   |   trials |   success_rate |   success_rate_ci_low |   success_rate_ci_high |   rate_403 |   source_unavailable_rate |   fallback_activation_rate |   fallback_ci_low |   fallback_ci_high |   recipes_mean |   recipes_median |   recipes_mean_ci_low |   recipes_mean_ci_high |   recipes_median_ci_low |   recipes_median_ci_high |   latency_p50_ms |   latency_p95_ms |   latency_median_ci_low |   latency_median_ci_high |   completeness_mean |   completeness_median |   completeness_mean_ci_low |   completeness_mean_ci_high |   availability_rate |   availability_ci_low |   availability_ci_high |
|:---------|---------:|---------------:|----------------------:|-----------------------:|-----------:|--------------------------:|---------------------------:|------------------:|-------------------:|---------------:|-----------------:|----------------------:|-----------------------:|------------------------:|-------------------------:|-----------------:|-----------------:|------------------------:|-------------------------:|--------------------:|----------------------:|---------------------------:|----------------------------:|--------------------:|----------------------:|-----------------------:|
| bbc      |        3 |              1 |              0.438503 |               1        |          0 |                         0 |                          0 |          0        |           0.561497 |              1 |                1 |                     1 |                      1 |                       1 |                        1 |          4687.97 |           5079.8 |                 4371.72 |                  5123.33 |                   1 |                     1 |                          1 |                           1 |                   1 |              0.438503 |               1        |
| serious  |        3 |              0 |              0        |               0.561497 |          1 |                         1 |                          1 |          0.438503 |           1        |              0 |                0 |                     0 |                      0 |                       0 |                        0 |         35187.8  |          54762.1 |                15709    |                 56937.1  |                 nan |                   nan |                        nan |                         nan |                   0 |              0        |               0.561497 |
| simply   |        3 |              1 |              0.438503 |               1        |          1 |                         0 |                          1 |          0.438503 |           1        |              1 |                1 |                     1 |                      1 |                       1 |                        1 |         41316.7  |          45017.1 |                33117.9  |                 45428.3  |                   1 |                     1 |                          1 |                           1 |                   1 |              0.438503 |               1        |

## Hypothesis Tests

| test                                 | metric             |   statistic |     p_value |   dof |   n_pairs |   improved_pairs |   regressed_pairs | note                          |
|:-------------------------------------|:-------------------|------------:|------------:|------:|----------:|-----------------:|------------------:|:------------------------------|
| kruskal_wallis                       | recipes_found      |     8       |   0.0183156 |   nan |       nan |              nan |               nan | nan                           |
| kruskal_wallis                       | latency_ms         |     5.42222 |   0.0664629 |   nan |       nan |              nan |               nan | nan                           |
| kruskal_wallis                       | completeness_score |   nan       | nan         |   nan |       nan |              nan |               nan | nan                           |
| chi_square_success_by_source         | success            |     9       |   0.011109  |     2 |       nan |              nan |               nan | nan                           |
| mcnemar_formatting_artifact_pre_post | artifact_binary    |     0       |   1         |   nan |         3 |                0 |                 0 | nan                           |
| logistic_regression                  | success            |   nan       | nan         |   nan |       nan |              nan |               nan | Model failed: Singular matrix |

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