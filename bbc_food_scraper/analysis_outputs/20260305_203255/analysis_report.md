# Statistical Analysis Report

Generated: 2026-03-05T21:04:43

## Descriptive Summary by Source

| source   |   trials |   success_rate |   success_rate_ci_low |   success_rate_ci_high |   rate_403 |   source_unavailable_rate |   fallback_activation_rate |   fallback_ci_low |   fallback_ci_high |   recipes_mean |   recipes_median |   recipes_mean_ci_low |   recipes_mean_ci_high |   recipes_median_ci_low |   recipes_median_ci_high |   latency_p50_ms |   latency_p95_ms |   latency_median_ci_low |   latency_median_ci_high |   completeness_mean |   completeness_median |   completeness_mean_ci_low |   completeness_mean_ci_high |   availability_rate |   availability_ci_low |   availability_ci_high |
|:---------|---------:|---------------:|----------------------:|-----------------------:|-----------:|--------------------------:|---------------------------:|------------------:|-------------------:|---------------:|-----------------:|----------------------:|-----------------------:|------------------------:|-------------------------:|-----------------:|-----------------:|------------------------:|-------------------------:|--------------------:|----------------------:|---------------------------:|----------------------------:|--------------------:|----------------------:|-----------------------:|
| bbc      |       10 |            1   |             0.722467  |               1        |          0 |                       0   |                          0 |          0        |           0.277533 |            2   |                2 |                     2 |                    2   |                       2 |                        2 |          11700.5 |          12295.7 |                 11249.1 |                  11979.5 |                   1 |                     1 |                          1 |                           1 |                 1   |             0.722467  |               1        |
| serious  |       10 |            0.2 |             0.0566822 |               0.509838 |          1 |                       0.8 |                          1 |          0.722467 |           1        |            0.4 |                0 |                     0 |                    1   |                       0 |                        1 |          57762.7 |         197379   |                 35971.9 |                 153087   |                   1 |                     1 |                          1 |                           1 |                 0.2 |             0.0566822 |               0.509838 |
| simply   |       10 |            0.3 |             0.107791  |               0.603222 |          1 |                       0.7 |                          1 |          0.722467 |           1        |            0.6 |                0 |                     0 |                    1.2 |                       0 |                        2 |          57573.3 |         157999   |                 15912.9 |                 141939   |                   1 |                     1 |                          1 |                           1 |                 0.3 |             0.107791  |               0.603222 |

## Hypothesis Tests

| test                                 | metric             |   statistic |       p_value |   dof |   n_pairs |   improved_pairs |   regressed_pairs | note                           |
|:-------------------------------------|:-------------------|------------:|--------------:|------:|----------:|-----------------:|------------------:|:-------------------------------|
| kruskal_wallis                       | recipes_found      |     14.6933 |   0.000644738 |   nan |       nan |              nan |               nan | nan                            |
| kruskal_wallis                       | latency_ms         |     19.3652 |   6.23604e-05 |   nan |       nan |              nan |               nan | nan                            |
| kruskal_wallis                       | completeness_score |    nan      | nan           |   nan |       nan |              nan |               nan | nan                            |
| chi_square_success_by_source         | success            |     15.2    |   0.000500451 |     2 |       nan |              nan |               nan | nan                            |
| mcnemar_formatting_artifact_pre_post | artifact_binary    |      0      |   0.03125     |   nan |        10 |                6 |                 0 | nan                            |
| wilcoxon_pre_post_binary_delta       | artifact_delta     |      0      |   0.03125     |   nan |       nan |              nan |               nan | nan                            |
| logistic_regression                  | success            |    nan      | nan           |   nan |       nan |              nan |               nan | Model failed: math range error |

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