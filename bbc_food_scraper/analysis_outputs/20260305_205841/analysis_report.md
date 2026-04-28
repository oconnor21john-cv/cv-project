# Statistical Analysis Report

Generated: 2026-03-05T21:15:26

## Descriptive Summary by Source

| source   |   trials |   success_rate |   success_rate_ci_low |   success_rate_ci_high |   rate_403 |   source_unavailable_rate |   fallback_activation_rate |   fallback_ci_low |   fallback_ci_high |   recipes_mean |   recipes_median |   recipes_mean_ci_low |   recipes_mean_ci_high |   recipes_median_ci_low |   recipes_median_ci_high |   latency_p50_ms |   latency_p95_ms |   latency_median_ci_low |   latency_median_ci_high |   completeness_mean |   completeness_median |   completeness_mean_ci_low |   completeness_mean_ci_high |   availability_rate |   availability_ci_low |   availability_ci_high |
|:---------|---------:|---------------:|----------------------:|-----------------------:|-----------:|--------------------------:|---------------------------:|------------------:|-------------------:|---------------:|-----------------:|----------------------:|-----------------------:|------------------------:|-------------------------:|-----------------:|-----------------:|------------------------:|-------------------------:|--------------------:|----------------------:|---------------------------:|----------------------------:|--------------------:|----------------------:|-----------------------:|
| bbc      |      100 |              1 |              0.963007 |              1         |          0 |                         0 |                          0 |          0        |          0.0369935 |              1 |                1 |                     1 |                      1 |                       1 |                        1 |          2509.01 |          3310.39 |                 2385.77 |                  2632.28 |                   1 |                     1 |                          1 |                           1 |                   1 |              0.963007 |              1         |
| serious  |      100 |              0 |              0        |              0.0369935 |          1 |                         1 |                          1 |          0.963007 |          1         |              0 |                0 |                     0 |                      0 |                       0 |                        0 |          3601.57 |          4691.43 |                 3521.48 |                  3714.11 |                 nan |                   nan |                        nan |                         nan |                   0 |              0        |              0.0369935 |
| simply   |      100 |              0 |              0        |              0.0369935 |          1 |                         1 |                          1 |          0.963007 |          1         |              0 |                0 |                     0 |                      0 |                       0 |                        0 |          3601.54 |          5241.67 |                 3452.06 |                  3707.9  |                 nan |                   nan |                        nan |                         nan |                   0 |              0        |              0.0369935 |

## Hypothesis Tests

| test                         | metric        |   statistic |       p_value |   dof | note                           |
|:-----------------------------|:--------------|------------:|--------------:|------:|:-------------------------------|
| kruskal_wallis               | recipes_found |     299     |   1.18297e-65 |   nan | nan                            |
| kruskal_wallis               | latency_ms    |     175.169 |   9.17429e-39 |   nan | nan                            |
| chi_square_success_by_source | success       |     300     |   7.1751e-66  |     2 | nan                            |
| logistic_regression          | success       |     nan     | nan           |   nan | Model failed: math range error |

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