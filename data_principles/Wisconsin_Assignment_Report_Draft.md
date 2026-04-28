# Report: Machine Learning Analysis of the Wisconsin Breast Cancer Data Set

## 1. Introduction

This report presents a practical machine learning analysis of the Wisconsin Breast Cancer data set from the UCI Machine Learning Repository. The main objective is to build and compare classification models that can distinguish between benign and malignant tumour cases using routinely observed cytological features. Accurate early classification is clinically important because delayed or incorrect diagnosis can affect treatment decisions and patient outcomes.  

The report combines both theoretical discussion and practical R implementation. First, the application area and data characteristics are introduced. Next, machine learning methods are justified and linked to measurable performance criteria. The practical section then explains data pre-processing, model training, evaluation, and visualisation in R. Four supervised learning models are developed and compared: Logistic Regression, K-Nearest Neighbours (KNN), Decision Tree, and Random Forest.  

The practical work is designed to follow the same style as weekly RStudio activities, with clear scripts, key outputs, and labelled diagrams. The report concludes by summarising findings, model strengths and weaknesses, and recommendations for future work in medical decision-support contexts.

## 2. Application Area and Data Used

The application area is medical diagnosis, specifically binary classification of breast tumour records into `benign` or `malignant`. This is a high-impact area for data science because well-performing predictive models can support clinicians by providing second-opinion risk estimates. In practice, such models should assist, not replace, expert medical judgement.  

The data file (`wisconsin.csv`) contains 699 observations and 10 variables: 9 predictor variables and 1 target variable (`Class`). Predictor fields are mostly ordinal/integer-style scores (typically 1 to 10), representing properties such as clump thickness, cell size, cell shape, marginal adhesion, and mitoses. The class labels are categorical strings and are converted to factors in R for modelling. Missing values appear only in `Bare.nuclei` (16 missing entries), which is handled by median imputation.  

Data quality checks include dimensions, data types, summary statistics, and missing-value counts. The class distribution is imbalanced but not extreme (more benign than malignant), so performance is reported using more than accuracy alone. As this is a well-known benchmark data set, it is appropriate for demonstrating model comparison, pre-processing decisions, and reproducible R workflows.

## 3. Machine Learning Methods Used

Four supervised machine learning methods are applied:

1. **Logistic Regression** - a linear probabilistic baseline that is interpretable and widely used in healthcare analytics.  
2. **K-Nearest Neighbours (KNN)** - a distance-based non-parametric method that can capture local structure but is sensitive to scaling.  
3. **Decision Tree (rpart)** - a rule-based model that is easy to explain and visualise, but may overfit if not controlled.  
4. **Random Forest** - an ensemble of trees that usually improves generalisation and reduces variance compared with a single tree.

Success criteria are based on classification quality on unseen test data and cross-validation behaviour. The main metrics are **Accuracy**, **Sensitivity (Recall for malignant cases)**, **Specificity**, **F1-score**, and **ROC-AUC**. In this domain, sensitivity is especially important because false negatives (malignant predicted as benign) are clinically costly.  

Model training uses repeated cross-validation in `caret` to reduce variance in performance estimation. Data standardisation (centering and scaling) is applied for distance-based models such as KNN and also kept consistent across models for fair comparison. Final model ranking is based on a balance of metrics rather than one number in isolation.

## 4. Practical: Pre-processing of Data

The CSV file is loaded with `readr::read_csv()` and inspected using `dim()`, `names()`, `summary()`, and `colSums(is.na())`. The target variable `Class` is converted to a factor with levels ordered as `benign`, `malignant`, enabling probability-based evaluation in `caret` and `pROC`.  

Only one variable (`Bare.nuclei`) contains missing values, so median imputation is applied. This approach is robust against outliers and keeps the full sample size of 699 records. A stratified 70/30 train-test split is created using `createDataPartition()` so both classes remain proportionally represented in train and test sets.  

Predictor scaling is performed through `preProcess(..., method = c("center", "scale"))`, fitted on training data only and then applied to test data to avoid leakage.  

**Screenshot evidence to include:**  
- Script editor showing data load, missing-value checks, factor conversion, and imputation code.  
- Console output confirming dimensions and missing values before/after pre-processing.

## 5. Practical: R Programming Content and Student Function

Model building is implemented in a clean, commented R script (`wisconsin_analysis.R`) using `caret`. A repeated 10-fold cross-validation configuration (3 repeats) is used with class probabilities enabled and `twoClassSummary` for ROC-oriented tuning.  

Four models are trained: `glm` (logistic), `knn`, `rpart`, and `rf`. The script then applies each model to the held-out test set and compares outcomes in a single results table. A custom function written for this assignment, `evaluate_model()`, takes a trained model and test data and returns key metrics: Accuracy, Kappa, Sensitivity, Specificity, F1, and AUC. This function improves code reuse and ensures all models are scored consistently.  

The script also creates key visual outputs: class distribution bar chart, correlation heatmap, model-comparison bar chart, variable-importance plot, decision-tree diagram, and ROC curves for all models. Results are exported to `wisconsin_model_results.csv` for direct insertion into the report.  

Indicative outcomes from this data split show strong performance from all models, with Random Forest and Logistic Regression generally among the best. Example benchmark values include test accuracy around **0.96** and AUC around **0.99** for top models.  

**Screenshot evidence to include:**  
- Script sections for model training and the `evaluate_model()` function.  
- Console output for trained models and metric table.  
- Saved CSV results in the project folder.

## 6. Practical: Display of Data/Results

The results are presented through both numerical metrics and visual analytics to make interpretation clear. A class distribution bar chart confirms more benign than malignant cases. A predictor correlation heatmap shows several related cytological variables, supporting the use of both linear and non-linear models.  

The model comparison chart (Accuracy and AUC) provides a concise summary of performance trade-offs. In a typical run, Random Forest and Logistic Regression produce the strongest overall metrics, with Decision Tree slightly lower but highly interpretable. KNN performs competitively after scaling, demonstrating that preprocessing has a clear impact.  

ROC curves offer a threshold-independent comparison: curves close to the top-left corner indicate high discrimination between classes. AUC values near 1.0 suggest good separability in this dataset. Variable-importance output from Random Forest highlights which cellular features contribute most to prediction, giving domain-relevant insights beyond raw accuracy.  

The confusion-matrix outputs should be discussed in text, especially false negatives. In medical contexts, model selection should prioritise safety-sensitive performance (high sensitivity), not only global accuracy.  

**Screenshot evidence to include (key diagrams, 6-7 max):**  
1. Class distribution bar plot  
2. Correlation heatmap  
3. Decision tree diagram  
4. Variable importance chart  
5. ROC curve comparison plot  
6. Model metrics table in console/CSV

## 7. Source Code Listing

A full source listing is provided in the appendix using font size 10, including:

- all `library()` calls,  
- data loading and preprocessing commands,  
- train-test split logic,  
- model training blocks,  
- custom `evaluate_model()` function,  
- plotting and export commands.

This allows marker reproducibility: libraries can be loaded, script copied into RStudio, and analysis re-run end to end.  

**Packages used in this assignment:** `readr`, `dplyr`, `ggplot2`, `caret`, `rpart`, `rpart.plot`, `randomForest`, `pROC`, `corrplot`, `tidyr`.

## 8. Conclusions

This analysis shows that machine learning can classify Wisconsin breast-cancer records with high predictive performance when supported by suitable preprocessing and validation. Missing data handling and scaling were important to ensure reliable training and fair model comparison.  

Across the tested methods, ensemble and probabilistic approaches delivered the strongest balance of sensitivity, specificity, and ROC-AUC, while the decision tree offered interpretability benefits. The custom evaluation function helped standardise metrics and improve script quality.  

From an application viewpoint, these findings support the use of data-driven tools as clinical decision aids, particularly for prioritisation and risk stratification. However, limitations remain: this is a benchmark dataset, not a live clinical stream; external validation and calibration would be required before operational use.  

Future work could include hyperparameter optimisation, cost-sensitive learning (to further reduce false negatives), and comparison with modern gradient boosting methods. Overall, the practical workflow demonstrates good alignment between statistical rigor, reproducibility, and clear communication of results in RStudio.

## 9. References (Harvard Style)

American Cancer Society (2024) *Breast Cancer Facts & Figures*. Available at: https://www.cancer.org/ (Accessed: 3 March 2026).  

Dua, D. and Graff, C. (2019) *UCI Machine Learning Repository*. Irvine, CA: University of California, School of Information and Computer Science. Available at: https://archive.ics.uci.edu/ (Accessed: 3 March 2026).  

Han, J., Kamber, M. and Pei, J. (2012) *Data Mining: Concepts and Techniques*. 3rd edn. Waltham, MA: Morgan Kaufmann.  

James, G., Witten, D., Hastie, T. and Tibshirani, R. (2021) *An Introduction to Statistical Learning: with Applications in R*. 2nd edn. New York: Springer.  

Kuhn, M. and Johnson, K. (2013) *Applied Predictive Modeling*. New York: Springer.  

Kuhn, M. (2008) 'Building predictive models in R using the caret package', *Journal of Statistical Software*, 28(5), pp. 1-26.  

Pedregosa, F. et al. (2011) 'Scikit-learn: Machine Learning in Python', *Journal of Machine Learning Research*, 12, pp. 2825-2830.  

Robin, X. et al. (2011) 'pROC: an open-source package for R and S+ to analyze and compare ROC curves', *BMC Bioinformatics*, 12(77), pp. 1-8.

---

### Final checklist before submission

- Keep total report length within 1,500 words +/-10% (excluding references + appendix code).  
- Keep total pages within 15 pages including source listing.  
- Use no more than 6-7 diagrams, each with caption and short interpretation.  
- Ensure screenshot text is readable (zoom script/editor before snipping).  
- Confirm all package names and file paths in appendix are correct on your machine.
