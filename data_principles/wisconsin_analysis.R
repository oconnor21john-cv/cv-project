# Wisconsin Breast Cancer (UCI) - Assignment Analysis Script
# Author: John (student)
# Purpose: End-to-end preprocessing, modelling, evaluation, and visualisation

# ----------------------------- #
# 1. Load required packages
# ----------------------------- #
required_packages <- c(
  "readr", "dplyr", "ggplot2", "caret", "rpart", "rpart.plot",
  "randomForest", "pROC", "corrplot", "tidyr"
)

missing_packages <- required_packages[!(required_packages %in% installed.packages()[, "Package"])]
if (length(missing_packages) > 0) {
  install.packages(missing_packages, dependencies = TRUE)
}

invisible(lapply(required_packages, library, character.only = TRUE))

# ----------------------------- #
# 2. Read and inspect data
# ----------------------------- #
set.seed(42)

# Robust path detection so script works from any working directory
get_script_dir <- function() {
  if (interactive() && requireNamespace("rstudioapi", quietly = TRUE) && rstudioapi::isAvailable()) {
    active_path <- rstudioapi::getActiveDocumentContext()$path
    if (nzchar(active_path)) {
      return(dirname(normalizePath(active_path, winslash = "/", mustWork = TRUE)))
    }
  }

  file_arg <- grep("^--file=", commandArgs(), value = TRUE)
  if (length(file_arg) > 0) {
    script_path <- sub("^--file=", "", file_arg[1])
    return(dirname(normalizePath(script_path, winslash = "/", mustWork = TRUE)))
  }

  normalizePath(getwd(), winslash = "/", mustWork = TRUE)
}

locate_wisconsin_csv <- function() {
  script_dir <- get_script_dir()
  candidate_paths <- c(
    file.path(script_dir, "wisconsin.csv"),
    file.path(script_dir, "data_principles", "wisconsin.csv"),
    file.path(getwd(), "wisconsin.csv"),
    file.path(getwd(), "data_principles", "wisconsin.csv"),
    "c:/Users/John/Documents/Comp Sci Msc/web/it3/data_principles/wisconsin.csv"
  )

  valid_paths <- candidate_paths[file.exists(candidate_paths)]
  if (length(valid_paths) > 0) {
    return(normalizePath(valid_paths[1], winslash = "/", mustWork = TRUE))
  }

  if (interactive()) {
    message("wisconsin.csv not found automatically. Please select the file manually.")
    selected <- utils::choose.files(
      default = "",
      caption = "Select wisconsin.csv",
      multi = FALSE
    )
    if (length(selected) > 0 && nzchar(selected) && file.exists(selected)) {
      return(normalizePath(selected, winslash = "/", mustWork = TRUE))
    }
  }

  stop("Could not locate wisconsin.csv. Set data_path manually to the full file path and run again.")
}

script_dir <- get_script_dir()
data_path <- locate_wisconsin_csv()
wisconsin <- read_csv(data_path, show_col_types = FALSE)

cat("\nDetected script directory:", script_dir, "\n")
cat("Using data file:", data_path, "\n")

cat("\nData dimensions:\n")
print(dim(wisconsin))

cat("\nColumn names:\n")
print(names(wisconsin))

cat("\nMissing values by column:\n")
print(colSums(is.na(wisconsin)))

cat("\nClass distribution:\n")
print(table(wisconsin$Class))

# ----------------------------- #
# 3. Pre-processing
# ----------------------------- #
# Convert target to factor with positive class last (required for twoClassSummary)
wisconsin <- wisconsin %>%
  mutate(
    Class = factor(Class, levels = c("benign", "malignant"))
  )

# Median imputation for Bare.nuclei (only column with missing values)
median_bare_nuclei <- median(wisconsin$Bare.nuclei, na.rm = TRUE)
wisconsin <- wisconsin %>%
  mutate(Bare.nuclei = ifelse(is.na(Bare.nuclei), median_bare_nuclei, Bare.nuclei))

cat("\nMissing values after imputation:\n")
print(colSums(is.na(wisconsin)))

# ----------------------------- #
# 4. Exploratory visualisations
# ----------------------------- #
# Class count plot
plot_class <- ggplot(wisconsin, aes(x = Class, fill = Class)) +
  geom_bar(width = 0.7) +
  scale_fill_manual(values = c("benign" = "#4DAF4A", "malignant" = "#E41A1C")) +
  labs(
    title = "Class Distribution",
    x = "Diagnosis Class",
    y = "Count"
  ) +
  theme_minimal(base_size = 12) +
  theme(legend.position = "none")

print(plot_class)

# Correlation heatmap for predictors
predictor_matrix <- wisconsin %>% select(-Class) %>% as.matrix()
corrplot(
  cor(predictor_matrix),
  method = "color",
  type = "upper",
  tl.col = "black",
  tl.cex = 0.8,
  title = "Correlation Heatmap of Predictors",
  mar = c(0, 0, 2, 0)
)

# ----------------------------- #
# 5. Train-test split
# ----------------------------- #
train_index <- createDataPartition(wisconsin$Class, p = 0.7, list = FALSE)
train_data <- wisconsin[train_index, ]
test_data <- wisconsin[-train_index, ]

cat("\nTrain size:", nrow(train_data), "\n")
cat("Test size:", nrow(test_data), "\n")

# Standardisation from training data only
preproc <- preProcess(train_data %>% select(-Class), method = c("center", "scale"))
train_x <- predict(preproc, train_data %>% select(-Class))
test_x <- predict(preproc, test_data %>% select(-Class))

train_processed <- cbind(train_x, Class = train_data$Class)
test_processed <- cbind(test_x, Class = test_data$Class)

# ----------------------------- #
# 6. Model training
# ----------------------------- #
ctrl <- trainControl(
  method = "repeatedcv",
  number = 10,
  repeats = 3,
  classProbs = TRUE,
  summaryFunction = twoClassSummary,
  savePredictions = "final"
)

# Logistic Regression
model_glm <- train(
  Class ~ ., data = train_processed,
  method = "glm",
  family = "binomial",
  trControl = ctrl,
  metric = "ROC"
)

# K-Nearest Neighbours
model_knn <- train(
  Class ~ ., data = train_processed,
  method = "knn",
  tuneLength = 10,
  trControl = ctrl,
  metric = "ROC"
)

# Decision Tree (rpart)
model_tree <- train(
  Class ~ ., data = train_processed,
  method = "rpart",
  tuneLength = 10,
  trControl = ctrl,
  metric = "ROC"
)

# Random Forest
model_rf <- train(
  Class ~ ., data = train_processed,
  method = "rf",
  tuneLength = 5,
  trControl = ctrl,
  metric = "ROC"
)

cat("\nCross-validated model summaries:\n")
print(model_glm)
print(model_knn)
print(model_tree)
print(model_rf)

# ----------------------------- #
# 7. Custom evaluation function
# ----------------------------- #
evaluate_model <- function(model, test_df, positive_class = "malignant") {
  preds <- predict(model, test_df)
  probs <- predict(model, test_df, type = "prob")[, positive_class]

  cm <- confusionMatrix(
    data = preds,
    reference = test_df$Class,
    positive = positive_class
  )

  roc_obj <- roc(
    response = test_df$Class,
    predictor = probs,
    levels = c("benign", "malignant"),
    direction = "<"
  )

  data.frame(
    Model = model$method,
    Accuracy = as.numeric(cm$overall["Accuracy"]),
    Kappa = as.numeric(cm$overall["Kappa"]),
    Sensitivity = as.numeric(cm$byClass["Sensitivity"]),
    Specificity = as.numeric(cm$byClass["Specificity"]),
    F1 = as.numeric(cm$byClass["F1"]),
    AUC = as.numeric(auc(roc_obj))
  )
}

results_glm <- evaluate_model(model_glm, test_processed)
results_knn <- evaluate_model(model_knn, test_processed)
results_tree <- evaluate_model(model_tree, test_processed)
results_rf <- evaluate_model(model_rf, test_processed)

all_results <- bind_rows(results_glm, results_knn, results_tree, results_rf) %>%
  mutate(
    Model = recode(
      Model,
      glm = "Logistic Regression",
      knn = "KNN",
      rpart = "Decision Tree",
      rf = "Random Forest"
    )
  ) %>%
  arrange(desc(Accuracy))

cat("\nTest-set performance table:\n")
print(all_results)

# ----------------------------- #
# 8. Important diagrams/outputs
# ----------------------------- #
# Plot model comparison by Accuracy
plot_results <- all_results %>%
  select(Model, Accuracy, AUC) %>%
  pivot_longer(cols = c(Accuracy, AUC), names_to = "Metric", values_to = "Value")

ggplot(plot_results, aes(x = Model, y = Value, fill = Metric)) +
  geom_col(position = position_dodge(width = 0.8), width = 0.7) +
  coord_cartesian(ylim = c(0.8, 1.0)) +
  labs(
    title = "Model Comparison on Test Data",
    y = "Score",
    x = "Model"
  ) +
  theme_minimal(base_size = 12)

# Variable importance from random forest
rf_varimp <- varImp(model_rf)
print(rf_varimp)
plot(rf_varimp, top = 10, main = "Top 10 Variable Importance (Random Forest)")

# Decision tree plot
rpart.plot(model_tree$finalModel, main = "Decision Tree Structure")

# ROC curves for all models on the test set
roc_glm <- roc(test_processed$Class, predict(model_glm, test_processed, type = "prob")[, "malignant"], levels = c("benign", "malignant"), direction = "<")
roc_knn <- roc(test_processed$Class, predict(model_knn, test_processed, type = "prob")[, "malignant"], levels = c("benign", "malignant"), direction = "<")
roc_tree <- roc(test_processed$Class, predict(model_tree, test_processed, type = "prob")[, "malignant"], levels = c("benign", "malignant"), direction = "<")
roc_rf <- roc(test_processed$Class, predict(model_rf, test_processed, type = "prob")[, "malignant"], levels = c("benign", "malignant"), direction = "<")

plot(roc_glm, col = "blue", lwd = 2, main = "ROC Curves - Model Comparison")
plot(roc_knn, col = "darkgreen", lwd = 2, add = TRUE)
plot(roc_tree, col = "orange", lwd = 2, add = TRUE)
plot(roc_rf, col = "red", lwd = 2, add = TRUE)
legend(
  "bottomright",
  legend = c(
    paste("Logistic Regression AUC =", round(auc(roc_glm), 3)),
    paste("KNN AUC =", round(auc(roc_knn), 3)),
    paste("Decision Tree AUC =", round(auc(roc_tree), 3)),
    paste("Random Forest AUC =", round(auc(roc_rf), 3))
  ),
  col = c("blue", "darkgreen", "orange", "red"),
  lwd = 2,
  cex = 0.8
)

# ----------------------------- #
# 9. Save table outputs for report
# ----------------------------- #
if (!exists("all_results")) {
  stop("all_results does not exist. Run the full script from the top before saving outputs.")
}

if (!exists("data_path") || !file.exists(data_path)) {
  data_path <- locate_wisconsin_csv()
}

output_dir <- dirname(normalizePath(data_path, winslash = "/", mustWork = TRUE))
output_path <- file.path(output_dir, "wisconsin_model_results.csv")
write.csv(all_results, output_path, row.names = FALSE)

cat("\nAnalysis complete.\n")
cat("Current working directory:", getwd(), "\n")
cat("Results saved to:", output_path, "\n")
