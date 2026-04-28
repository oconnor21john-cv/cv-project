# ========================
# Import Libraries
# ========================
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split, KFold, cross_val_score
from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import (precision_score, recall_score, f1_score, roc_auc_score, accuracy_score, roc_curve, classification_report, confusion_matrix)
import random
from sklearn.metrics import ConfusionMatrixDisplay
from sklearn.inspection import permutation_importance
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
import tensorflow.keras as keras


# ========================
# Reproducibility Setup
# ========================
random.seed(42)
np.random.seed(42)
tf.random.set_seed(42)

# ========================
# Section 1: Data Preparation
# ========================
print("Loading and preprocessing data...")
# Load the dataset
data = pd.read_csv('as1-bank.csv')

# Separate features and target
X = data.drop('y', axis=1)
y = data['y'].replace({'no': 0, 'yes': 1})  # Convert target to binary

# Split the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Convert pandas Series to numpy arrays for easier indexing
y_train = y_train.values
y_test = y_test.values

# Identify numerical and categorical columns
numerical_cols = ['age', 'balance', 'duration', 'campaign', 'pdays', 'previous']
categorical_cols = ['marital', 'education', 'default', 'housing', 'loan', 'contact', 'poutcome']

print(f"Categorical features: {categorical_cols}")
print(f"Numerical features: {numerical_cols}")

# ========================
# Feature Set Definitions
# ========================
feature_sets = {
    "all_features": numerical_cols + categorical_cols,
    "only_numerical": numerical_cols,
    "financial_focus": ['balance', 'duration', 'pdays', 'previous']  # Domain-specific selection
}

# ========================
# Section 2: Hyperparameter Definitions
# ========================
architectures = [
    (10,),         # 1 layer, 10 neurons
    (50,),         # 1 layer, 50 neurons
    (100,),        # 1 layer, 100 neurons
    (30, 20),      # 2 layers: 30 → 20
    (50, 30),      # 2 layers: 50 → 30
    (100, 50),     # 2 layers: 100 → 50
    (100, 80, 50), # 3 layers: 100 → 80 → 50
    (150, 100, 50) # 3 layers: 150 → 100 → 50
]

learning_rates = [0.0001, 0.001, 0.01, 0.1]  # Learning rates to test

# Cross-validation setup
kfold = KFold(n_splits=5, shuffle=True, random_state=42)

# ========================
# Section 3: Experiment Loop (Feature Sets + Architectures + Learning Rates)
# ========================
print("\nRunning experiments with different feature sets, architectures, and learning rates...")
results = []
best_cv_f1 = -1
best_model_info = {}
best_preprocessor = None

# Define early stopping
early_stopping = keras.callbacks.EarlyStopping(
    monitor='val_loss',
    patience=10,
    restore_best_weights=True
)

for set_name, features in feature_sets.items():
    print(f"\n{'='*50}")
    print(f"Processing feature set: {set_name}")
    print(f"Features: {features}")
    print(f"{'='*50}")
    
    # Subset features
    X_train_sub = X_train[features]
    X_test_sub = X_test[features]
    
    # Identify numerical/categorical features in this set
    num_in_set = [col for col in numerical_cols if col in features]
    cat_in_set = [col for col in categorical_cols if col in features]
    
    print(f"  Numerical features: {num_in_set}")
    print(f"  Categorical features: {cat_in_set}")
    print(f"  Total features: {len(num_in_set)} numerical + {len(cat_in_set)} categorical")
    
    # Create preprocessor for this feature set
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), num_in_set),
            ('cat', OneHotEncoder(handle_unknown='ignore'), cat_in_set)
        ])
    
    # Preprocess subset
    X_train_prep = preprocessor.fit_transform(X_train_sub)
    X_test_prep = preprocessor.transform(X_test_sub)
    
    # Convert to dense arrays for TensorFlow
    if hasattr(X_train_prep, 'toarray'):
        X_train_prep = X_train_prep.toarray()
        X_test_prep = X_test_prep.toarray()
    
    # Convert to numpy arrays for easier indexing in k-fold
    X_train_prep = np.array(X_train_prep)
    X_test_prep = np.array(X_test_prep)
    
    # Get feature count after one-hot encoding
    if len(cat_in_set) > 0:
        cat_encoder = preprocessor.named_transformers_['cat']
        n_cat_features = sum(len(cat_encoder.categories_[i]) for i in range(len(cat_in_set)))
    else:
        n_cat_features = 0
        
    total_features = len(num_in_set) + n_cat_features
    print(f"  Total features after encoding: {total_features}")
    
    for arch in architectures:
        for lr in learning_rates:
            print(f"\nTesting architecture {arch} with learning rate {lr} and {set_name}")
            
            # Perform k-fold cross-validation
            cv_scores = []
            cv_histories = []
            
            for fold, (train_idx, val_idx) in enumerate(kfold.split(X_train_prep)):
                print(f"  Fold {fold+1}/5", end=" ")
                
                # Split data for this fold
                X_fold_train, X_fold_val = X_train_prep[train_idx], X_train_prep[val_idx]
                y_fold_train, y_fold_val = y_train[train_idx], y_train[val_idx]
                
                # Build model for this fold
                model = keras.Sequential()
                model.add(keras.layers.Input(shape=(X_train_prep.shape[1],)))
                
                for units in arch:
                    model.add(keras.layers.Dense(units, activation='relu'))
                    model.add(keras.layers.BatchNormalization())
                    model.add(keras.layers.Dropout(0.3))
                
                model.add(keras.layers.Dense(1, activation='sigmoid'))
                
                # Compile with current learning rate
                model.compile(
                    optimizer=keras.optimizers.SGD(learning_rate=lr),
                    loss='binary_crossentropy',
                    metrics=[
                        'accuracy',
                        keras.metrics.Precision(name='precision'),
                        keras.metrics.Recall(name='recall')
                    ]
                )
                
                # Train with early stopping
                history = model.fit(
                    X_fold_train,
                    y_fold_train,
                    epochs=100,
                    batch_size=32,
                    validation_data=(X_fold_val, y_fold_val),
                    callbacks=[early_stopping],
                    verbose=0
                )
                
                # Extract best validation metrics
                best_epoch = np.argmin(history.history['val_loss'])
                val_acc = history.history['val_accuracy'][best_epoch]
                val_precision = history.history['val_precision'][best_epoch]
                val_recall = history.history['val_recall'][best_epoch]
                val_f1 = 2 * (val_precision * val_recall) / (val_precision + val_recall + 1e-7)
                
                cv_scores.append(val_f1)
                cv_histories.append(history)
                print(f"F1: {val_f1:.4f}")
            
            # Calculate mean and std of cross-validation scores
            mean_cv_f1 = np.mean(cv_scores)
            std_cv_f1 = np.std(cv_scores)
            
            # Store results
            results.append({
                'feature_set': set_name,
                'architecture': str(arch),
                'learning_rate': lr,
                'cv_f1_mean': mean_cv_f1,
                'cv_f1_std': std_cv_f1,
                'cv_f1_scores': cv_scores,
                'n_features': total_features
            })
            
            print(f"  CV F1: {mean_cv_f1:.4f} ± {std_cv_f1:.4f}")
            
            # Track best model (cross-validation performance)
            if mean_cv_f1 > best_cv_f1:
                best_cv_f1 = mean_cv_f1
                best_model_info = {
                    'feature_set': set_name,
                    'architecture': arch,
                    'learning_rate': lr,
                    'preprocessor': preprocessor,
                    'cv_scores': cv_scores,
                    'cv_histories': cv_histories
                }
                print(f"  🏆 New best model! CV F1: {mean_cv_f1:.4f}")

# Save results for report
results_df = pd.DataFrame(results)
results_df.to_csv('experiment_results.csv', index=False)
print("\nSaved experiment results to 'experiment_results.csv'")

# Display cross-validation results summary
print("\n" + "="*80)
print("CROSS-VALIDATION RESULTS SUMMARY")
print("="*80)

# Find top 5 configurations
top_configs = results_df.nlargest(5, 'cv_f1_mean')
print("\nTop 5 Configurations:")
print(top_configs[['feature_set', 'architecture', 'learning_rate', 'cv_f1_mean', 'cv_f1_std']].to_string(index=False))

# Learning rate analysis
print("\n" + "-"*50)
print("LEARNING RATE ANALYSIS")
print("-"*50)
lr_analysis = results_df.groupby('learning_rate')['cv_f1_mean'].agg(['mean', 'std', 'count']).round(4)
print(lr_analysis)

# Architecture analysis
print("\n" + "-"*50)
print("ARCHITECTURE ANALYSIS")
print("-"*50)
arch_analysis = results_df.groupby('architecture')['cv_f1_mean'].agg(['mean', 'std', 'count']).round(4)
print(arch_analysis)

# Feature set analysis
print("\n" + "-"*50)
print("FEATURE SET ANALYSIS")
print("-"*50)
feature_analysis = results_df.groupby('feature_set')['cv_f1_mean'].agg(['mean', 'std', 'count']).round(4)
print(feature_analysis)

# ========================
# Section 4: Final Model Training & Baseline
# ========================
print("\nTraining final model with best configuration...")
best_set = best_model_info['feature_set']
best_arch = best_model_info['architecture']
best_lr = best_model_info['learning_rate']
preprocessor = best_model_info['preprocessor']

print(f"\nBest configuration:")
print(f"  Feature set: {best_set}")
print(f"  Architecture: {best_arch}")
print(f"  Learning rate: {best_lr}")
print(f"  Cross-validation F1: {best_cv_f1:.4f}")

# Prepare best feature data
X_train_best = X_train[feature_sets[best_set]]
X_test_best = X_test[feature_sets[best_set]]

# Preprocess with best preprocessor
X_train_prep = preprocessor.transform(X_train_best)
X_test_prep = preprocessor.transform(X_test_best)

# Convert to numpy arrays
X_train_prep = np.array(X_train_prep)
X_test_prep = np.array(X_test_prep)

# Convert to dense
if hasattr(X_train_prep, 'toarray'):
    X_train_prep = X_train_prep.toarray()
    X_test_prep = X_test_prep.toarray()

# Verify feature dimensions
print(f"\nFeature dimensions:")
print(f"  Training: {X_train_prep.shape[1]} features")
print(f"  Testing:  {X_test_prep.shape[1]} features")
assert X_train_prep.shape[1] == X_test_prep.shape[1], "Feature dimension mismatch!"

# Build final model (same architecture)
final_model = keras.Sequential()
final_model.add(keras.layers.Input(shape=(X_train_prep.shape[1],)))

for units in best_arch:
    final_model.add(keras.layers.Dense(units, activation='relu'))
    final_model.add(keras.layers.BatchNormalization())
    final_model.add(keras.layers.Dropout(0.3))

final_model.add(keras.layers.Dense(1, activation='sigmoid'))

final_model.compile(
    optimizer=keras.optimizers.SGD(learning_rate=best_lr),  # Keep SGD
    loss='binary_crossentropy',
    metrics=['accuracy', keras.metrics.Precision(), keras.metrics.Recall()]
)

# Train on full training data
history = final_model.fit(
    X_train_prep,
    y_train,
    epochs=100,
    batch_size=32,
    validation_data=(X_test_prep, y_test),
    callbacks=[early_stopping],
    verbose=1
)

# ========================
# Section 5: Evaluation and Visualization
# ========================
print("\nEvaluating final model...")

# Generate predictions
y_pred = (final_model.predict(X_test_prep) > 0.5).astype("int32").flatten()
y_proba = final_model.predict(X_test_prep).flatten()

# Evaluate performance
print("\n" + "="*50)
print(f"Best Configuration: {best_set} features with {best_arch} architecture")
print("="*50)
print("Classification Report:")
print(classification_report(y_test, y_pred))

# Visualize confusion matrix
plt.figure(figsize=(8, 6))
ConfusionMatrixDisplay.from_predictions(y_test, y_pred, cmap='Blues')
plt.title('Confusion Matrix')
plt.savefig('confusion_matrix.png')
plt.show()

# Save confusion matrix data
cm = confusion_matrix(y_test, y_pred)
cm_df = pd.DataFrame(cm, 
                     columns=['Predicted Negative', 'Predicted Positive'],
                     index=['Actual Negative', 'Actual Positive'])
cm_df.to_csv('confusion_matrix_data.csv')
print("Confusion matrix data saved to 'confusion_matrix_data.csv'")

print(f"ROC AUC: {roc_auc_score(y_test, y_proba):.4f}")

# Save ROC curve data
fpr, tpr, thresholds = roc_curve(y_test, y_proba)
roc_data = pd.DataFrame({
    'False_Positive_Rate': fpr,
    'True_Positive_Rate': tpr,
    'Thresholds': thresholds
})
roc_data.to_csv('roc_curve_data.csv')
print("ROC curve data saved to 'roc_curve_data.csv'")

# Plot ROC curve
plt.figure(figsize=(8, 6))
plt.plot(fpr, tpr, label=f'ROC Curve (AUC = {roc_auc_score(y_test, y_proba):.4f})')
plt.plot([0, 1], [0, 1], 'k--', label='Random Classifier')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve')
plt.legend()
plt.savefig('roc_curve.png')
plt.show()

# ========================
# Feature Importance Analysis
# ========================
print("\nCalculating feature importance...")

# Create a custom scoring function that uses class predictions
from sklearn.metrics import make_scorer, f1_score

def f1_scorer(y_true, y_pred):
    """Custom scorer that converts probabilities to class predictions"""
    # Convert probabilities to binary predictions
    y_pred_binary = (y_pred > 0.5).astype("int32")
    return f1_score(y_true, y_pred_binary)

# Create a custom estimator wrapper for TensorFlow model
class TFModelWrapper:
    def __init__(self, model):
        self.model = model
    
    def fit(self, X, y):
        # Dummy fit method - the model is already trained
        return self
    
    def predict(self, X):
        # Get probabilities and convert to binary predictions
        probas = self.model.predict(X, verbose=0)
        return (probas > 0.5).astype(int)
    
    def predict_proba(self, X):
        # Return probabilities as a 2D array
        probas = self.model.predict(X, verbose=0)
        # Convert to 2D array: [1-p, p] for each sample
        return np.column_stack([1-probas, probas])

# Wrap the TensorFlow model
wrapped_model = TFModelWrapper(final_model)

# Use the standard f1_score with the wrapped model
scorer = make_scorer(f1_score)

# Calculate permutation importance
result = permutation_importance(
    wrapped_model, 
    X_test_prep, 
    y_test,
    scoring=scorer,
    n_repeats=5,
    random_state=42,
    n_jobs=-1
)

# Get feature names
if 'num' in preprocessor.named_transformers_:
    num_features = preprocessor.transformers_[0][2]
else:
    num_features = []
    
if 'cat' in preprocessor.named_transformers_:
    cat_encoder = preprocessor.named_transformers_['cat']
    # Get original categorical features in this set
    cat_in_set = [col for col in categorical_cols if col in feature_sets[best_set]]
    cat_features = cat_encoder.get_feature_names_out(cat_in_set)
else:
    cat_features = []

all_features = list(num_features) + list(cat_features)

# Plot importance
plt.figure(figsize=(12, 8))
importances_mean = result.importances_mean
sorted_idx = importances_mean.argsort()
plt.barh(np.array(all_features)[sorted_idx], importances_mean[sorted_idx])
plt.title(f"Permutation Importance ({best_set} features)")
plt.xlabel("F1 Score Decrease")
plt.tight_layout()
plt.savefig('feature_importance.png')
plt.show()

# Save feature importance data
feature_importance_data = pd.DataFrame({
    'Feature': all_features,
    'Importance_Mean': importances_mean,
    'Importance_Std': result.importances_std
})
feature_importance_data = feature_importance_data.sort_values('Importance_Mean', ascending=True)
feature_importance_data.to_csv('feature_importance_data.csv', index=False)
print("Feature importance data saved to 'feature_importance_data.csv'")

# ========================
# Results Comparison Table
# ========================
dummy = DummyClassifier(strategy='most_frequent')
dummy.fit(X_train_prep, y_train)
baseline_acc = dummy.score(X_test_prep, y_test)

comparison = pd.DataFrame({
    'Model': ['Baseline', 'Final ANN'],
    'Accuracy': [baseline_acc, accuracy_score(y_test, y_pred)],
    'Precision': [np.nan, precision_score(y_test, y_pred)],
    'Recall': [np.nan, recall_score(y_test, y_pred)],
    'F1': [np.nan, f1_score(y_test, y_pred)],
    'ROC AUC': [np.nan, roc_auc_score(y_test, y_proba)]
})

print("\nModel Comparison:")
print(comparison)
comparison.to_csv('model_comparison.csv', index=False)

# Plot training history for best model
plt.figure(figsize=(12, 5))

# Plot loss
plt.subplot(1, 2, 1)
plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.title('Training and Validation Loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()

# Plot accuracy
plt.subplot(1, 2, 2)
plt.plot(history.history['accuracy'], label='Training Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.title('Training and Validation Accuracy')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend()

plt.tight_layout()
plt.savefig('training_history.png')
plt.show()

# Save training history data
training_history_data = pd.DataFrame({
    'Epoch': range(1, len(history.history['loss']) + 1),
    'Training_Loss': history.history['loss'],
    'Validation_Loss': history.history['val_loss'],
    'Training_Accuracy': history.history['accuracy'],
    'Validation_Accuracy': history.history['val_accuracy']
})
training_history_data.to_csv('training_history_data.csv', index=False)
print("Training history data saved to 'training_history_data.csv'")