# Statistical Analysis Report

Generated: 2026-03-05T21:23:07

## Descriptive Summary by Source

| source   |   trials |   success_rate |   success_rate_ci_low |   success_rate_ci_high |   rate_403 |   source_unavailable_rate |   fallback_activation_rate |   fallback_ci_low |   fallback_ci_high |   recipes_mean |   recipes_median |   recipes_mean_ci_low |   recipes_mean_ci_high |   recipes_median_ci_low |   recipes_median_ci_high |   latency_p50_ms |   latency_p95_ms |   latency_median_ci_low |   latency_median_ci_high |   completeness_mean |   completeness_median |   completeness_mean_ci_low |   completeness_mean_ci_high |   availability_rate |   availability_ci_low |   availability_ci_high |
|:---------|---------:|---------------:|----------------------:|-----------------------:|-----------:|--------------------------:|---------------------------:|------------------:|-------------------:|---------------:|-----------------:|----------------------:|-----------------------:|------------------------:|-------------------------:|-----------------:|-----------------:|------------------------:|-------------------------:|--------------------:|----------------------:|---------------------------:|----------------------------:|--------------------:|----------------------:|-----------------------:|
| bbc      |       20 |           1    |             0.838875  |               1        |          0 |                      0    |                          0 |          0        |           0.161125 |           2    |                2 |                   2   |                    2   |                       2 |                        2 |          11714.6 |          12711.9 |                 11324.5 |                  12084.3 |                   1 |                     1 |                          1 |                           1 |                1    |             0.838875  |               1        |
| serious  |       20 |           0.2  |             0.0806577 |               0.416017 |          1 |                      0.8  |                          1 |          0.838875 |           1        |           0.35 |                0 |                   0.1 |                    0.7 |                       0 |                        0 |          57981.2 |         175115   |                 56940.6 |                  59593.6 |                   1 |                     1 |                          1 |                           1 |                0.2  |             0.0806577 |               0.416017 |
| simply   |       20 |           0.15 |             0.0523687 |               0.360419 |          1 |                      0.85 |                          1 |          0.838875 |           1        |           0.3  |                0 |                   0   |                    0.6 |                       0 |                        0 |          57175.5 |         125180   |                 56965.8 |                  57771.3 |                   1 |                     1 |                          1 |                           1 |                0.15 |             0.0523687 |               0.360419 |

## Hypothesis Tests

| test                                 | metric             |   statistic |       p_value |   dof |   n_pairs |   improved_pairs |   regressed_pairs | note                           |
|:-------------------------------------|:-------------------|------------:|--------------:|------:|----------:|-----------------:|------------------:|:-------------------------------|
| kruskal_wallis                       | recipes_found      |     37.8093 |   6.16345e-09 |   nan |       nan |              nan |               nan | nan                            |
| kruskal_wallis                       | latency_ms         |     39.8954 |   2.17181e-09 |   nan |       nan |              nan |               nan | nan                            |
| kruskal_wallis                       | completeness_score |    nan      | nan           |   nan |       nan |              nan |               nan | nan                            |
| chi_square_success_by_source         | success            |     36.7677 |   1.03753e-08 |     2 |       nan |              nan |               nan | nan                            |
| mcnemar_formatting_artifact_pre_post | artifact_binary    |      0      |   0.0078125   |   nan |        13 |                8 |                 0 | nan                            |
| wilcoxon_pre_post_binary_delta       | artifact_delta     |      0      |   0.0078125   |   nan |       nan |              nan |               nan | nan                            |
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