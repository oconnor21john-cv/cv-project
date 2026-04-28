
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import cross_val_score

# ========================
# Section 1: Data Preparation
# ========================
print("Loading and preprocessing data...")
# Load the dataset
data = pd.read_csv('as1-bank.csv')

# Separate features and target
X = data.drop('y', axis=1)
y = data['y'].map({'no': 0, 'yes': 1})  # Convert target to binary

# Split the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Identify numerical and categorical columns
numerical_cols = ['age', 'balance', 'duration', 'campaign', 'pdays', 'previous']
categorical_cols = ['marital', 'education', 'default', 'housing', 'loan', 'contact', 'poutcome']

# Define preprocessing pipeline
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numerical_cols),
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_cols)
    ])

# Create full pipeline that includes preprocessing
full_pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor)
])

# Preprocess data
X_train_preprocessed = full_pipeline.fit_transform(X_train)
X_test_preprocessed = full_pipeline.transform(X_test)

# Convert to dense arrays for TensorFlow
X_train_preprocessed = X_train_preprocessed.toarray() if hasattr(X_train_preprocessed, 'toarray') else X_train_preprocessed
X_test_preprocessed = X_test_preprocessed.toarray() if hasattr(X_test_preprocessed, 'toarray') else X_test_preprocessed

print(f"Preprocessed training shape: {X_train_preprocessed.shape}")
print(f"Preprocessed testing shape: {X_test_preprocessed.shape}")



///Output 
Loading and preprocessing data...
Preprocessed training shape: (6273, 23)
Preprocessed testing shape: (1569, 23)

# ========================
# Section 2: Architecture Definitions
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

# ========================
# Section 3: Architecture Comparison with TensorFlow
# ========================
print("\nEvaluating different architectures with TensorFlow...")
best_score = -1
best_arch = None
history_dict = {}

# Define early stopping callback
early_stopping = tf.keras.callbacks.EarlyStopping(
    monitor='val_loss',
    patience=10,
    restore_best_weights=True
)

# Create TensorBoard callback (optional)
# tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir="./logs")

for i, arch in enumerate(architectures):
    print(f"\nEvaluating architecture {i+1}/{len(architectures)}: {arch}")
    
    # Build model
    model = tf.keras.Sequential()
    model.add(tf.keras.layers.Input(shape=(X_train_preprocessed.shape[1],)))
    
    # Add hidden layers
    for units in arch:
        model.add(tf.keras.layers.Dense(units, activation='relu'))
        model.add(tf.keras.layers.BatchNormalization())
        model.add(tf.keras.layers.Dropout(0.3))
    
    # Add output layer
    model.add(tf.keras.layers.Dense(1, activation='sigmoid'))
    
    # Compile model
    model.compile(
        optimizer=tf.keras.optimizers.SGD(learning_rate=0.001),
        loss='binary_crossentropy',
        metrics=['accuracy', tf.keras.metrics.Precision(), tf.keras.metrics.Recall()]
    )
    
    # Train model
    history = model.fit(
        X_train_preprocessed,
        y_train,
        epochs=100,
        batch_size=32,
        validation_split=0.2,
        callbacks=[early_stopping],
        verbose=0
    )
    
    # Store history for later visualization
    history_dict[arch] = history
    
    # Evaluate on validation set
    val_loss, val_acc, val_precision, val_recall = model.evaluate(
        X_test_preprocessed, y_test, verbose=0
    )
    
    # Calculate F1 score
    val_f1 = 2 * (val_precision * val_recall) / (val_precision + val_recall + 1e-7)
    
    print(f"Architecture {arch}:")
    print(f"  Validation Accuracy: {val_acc:.4f}, F1: {val_f1:.4f}")
    
    if val_f1 > best_score:
        best_score = val_f1
        best_arch = arch
        best_model = model

print(f"\nBest Architecture: {best_arch} with F1: {best_score:.4f}")

///output
"Evaluating different architectures with TensorFlow...

Evaluating architecture 1/8: (10,)
Architecture (10,):
  Validation Accuracy: 0.8394, F1: 0.5987

Evaluating architecture 2/8: (50,)
Architecture (50,):
  Validation Accuracy: 0.8305, F1: 0.5804

Evaluating architecture 3/8: (100,)
Architecture (100,):
  Validation Accuracy: 0.8324, F1: 0.6009

Evaluating architecture 4/8: (30, 20)
Architecture (30, 20):
  Validation Accuracy: 0.8324, F1: 0.5696

Evaluating architecture 5/8: (50, 30)
Architecture (50, 30):
  Validation Accuracy: 0.8337, F1: 0.5978

Evaluating architecture 6/8: (100, 50)
Architecture (100, 50):
  Validation Accuracy: 0.8317, F1: 0.5913

Evaluating architecture 7/8: (100, 80, 50)
Architecture (100, 80, 50):
  Validation Accuracy: 0.8324, F1: 0.5667

Evaluating architecture 8/8: (150, 100, 50)
Architecture (150, 100, 50):
  Validation Accuracy: 0.8324, F1: 0.6009

Best Architecture: (100,) with F1: 0.6009"

# ========================
# Section 4: Training Best Model
# ========================
print("\nTraining final model with best architecture...")
# Best model is already trained during evaluation, but we can retrain on full data
final_model = tf.keras.models.clone_model(best_model)
final_model.compile(
    optimizer=tf.keras.optimizers.SGD(learning_rate=0.001),
    loss='binary_crossentropy',
    metrics=['accuracy', tf.keras.metrics.Precision(), tf.keras.metrics.Recall()]
)

# Train on full dataset
history = final_model.fit(
    X_train_preprocessed,
    y_train,
    epochs=100,
    batch_size=32,
    validation_data=(X_test_preprocessed, y_test),
    callbacks=[early_stopping],
    verbose=1
)
///output
Training final model with best architecture...
Epoch 1/100
[1m197/197[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m1s[0m 3ms/step - accuracy: 0.5848 - loss: 0.7768 - precision_8: 0.3106 - recall_8: 0.6562 - val_accuracy: 0.7342 - val_loss: 0.5930 - val_precision_8: 0.4488 - val_recall_8: 0.6657
Epoch 2/100
[1m197/197[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 2ms/step - accuracy: 0.6543 - loss: 0.6743 - precision_8: 0.3648 - recall_8: 0.6837 - val_accuracy: 0.7635 - val_loss: 0.5426 - val_precision_8: 0.4913 - val_recall_8: 0.7044
Epoch 3/100
[1m197/197[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 2ms/step - accuracy: 0.6916 - loss: 0.6284 - precision_8: 0.3907 - recall_8: 0.6586 - val_accuracy: 0.7750 - val_loss: 0.5127 - val_precision_8: 0.5090 - val_recall_8: 0.7017
Epoch 4/100
[1m197/197[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 2ms/step - accuracy: 0.7199 - loss: 0.5790 - precision_8: 0.4232 - recall_8: 0.6776 - val_accuracy: 0.7890 - val_loss: 0.4888 - val_precision_8: 0.5341 - val_recall_8: 0.6713
Epoch 5/100
[1m197/197[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 2ms/step - accuracy: 0.7613 - loss: 0.5353 - precision_8: 0.4812 - recall_8: 0.6761 - val_accuracy: 0.7929 - val_loss: 0.4703 - val_precision_8: 0.5416 - val_recall_8: 0.6657
Epoch 6/100
[1m197/197[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 2ms/step - accuracy: 0.7697 - loss: 0.5246 - precision_8: 0.4997 - recall_8: 0.6650 - val_accuracy: 0.7948 - val_loss: 0.4583 - val_precision_8: 0.5461 - val_recall_8: 0.6547
Epoch 7/100
[1m197/197[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 2ms/step - accuracy: 0.7783 - loss: 0.5024 - precision_8: 0.5011 - recall_8: 0.6470 - val_accuracy: 0.8075 - val_loss: 0.4425 - val_precision_8: 0.5754 - val_recall_8: 0.6326
Epoch 8/100
[1m197/197[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m1s[0m 3ms/step - accuracy: 0.7785 - loss: 0.4867 - precision_8: 0.4996 - recall_8: 0.6357 - val_accuracy: 0.8107 - val_loss: 0.4343 - val_precision_8: 0.5831 - val_recall_8: 0.6298
Epoch 9/100
[1m197/197[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 2ms/step - accuracy: 0.7864 - loss: 0.4722 - precision_8: 0.5183 - recall_8: 0.6420 - val_accuracy: 0.8101 - val_loss: 0.4234 - val_precision_8: 0.5842 - val_recall_8: 0.6133
Epoch 10/100
[1m197/197[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 2ms/step - accuracy: 0.7968 - loss: 0.4666 - precision_8: 0.5519 - recall_8: 0.6278 - val_accuracy: 0.8126 - val_loss: 0.4179 - val_precision_8: 0.5914 - val_recall_8: 0.6077
Epoch 11/100
[1m197/197[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 2ms/step - accuracy: 0.7950 - loss: 0.4634 - precision_8: 0.5305 - recall_8: 0.6157 - val_accuracy: 0.8152 - val_loss: 0.4098 - val_precision_8: 0.6000 - val_recall_8: 0.5967
Epoch 12/100
[1m197/197[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 2ms/step - accuracy: 0.8009 - loss: 0.4568 - precision_8: 0.5510 - recall_8: 0.5961 - val_accuracy: 0.8133 - val_loss: 0.4084 - val_precision_8: 0.5956 - val_recall_8: 0.5939
Epoch 13/100
[1m197/197[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 2ms/step - accuracy: 0.7981 - loss: 0.4549 - precision_8: 0.5602 - recall_8: 0.5715 - val_accuracy: 0.8133 - val_loss: 0.4038 - val_precision_8: 0.5961 - val_recall_8: 0.5912
Epoch 14/100
[1m197/197[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 2ms/step - accuracy: 0.8004 - loss: 0.4457 - precision_8: 0.5682 - recall_8: 0.6003 - val_accuracy: 0.8209 - val_loss: 0.3987 - val_precision_8: 0.6167 - val_recall_8: 0.5912
Epoch 15/100
[1m197/197[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 2ms/step - accuracy: 0.8187 - loss: 0.4334 - precision_8: 0.6072 - recall_8: 0.6035 - val_accuracy: 0.8222 - val_loss: 0.3951 - val_precision_8: 0.6231 - val_recall_8: 0.5801
Epoch 16/100
[1m197/197[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 2ms/step - accuracy: 0.8151 - loss: 0.4260 - precision_8: 0.5885 - recall_8: 0.5835 - val_accuracy: 0.8215 - val_loss: 0.3921 - val_precision_8: 0.6235 - val_recall_8: 0.5718
Epoch 17/100
[1m197/197[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 2ms/step - accuracy: 0.8087 - loss: 0.4236 - precision_8: 0.5839 - recall_8: 0.5878 - val_accuracy: 0.8222 - val_loss: 0.3905 - val_precision_8: 0.6246 - val_recall_8: 0.5746
Epoch 18/100
[1m197/197[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 2ms/step - accuracy: 0.8113 - loss: 0.4176 - precision_8: 0.5926 - recall_8: 0.5820 - val_accuracy: 0.8228 - val_loss: 0.3892 - val_precision_8: 0.6265 - val_recall_8: 0.5746
Epoch 19/100
[1m197/197[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 2ms/step - accuracy: 0.8147 - loss: 0.4220 - precision_8: 0.5872 - recall_8: 0.5816 - val_accuracy: 0.8266 - val_loss: 0.3868 - val_precision_8: 0.6389 - val_recall_8: 0.5718
Epoch 20/100
[1m197/197[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 2ms/step - accuracy: 0.8145 - loss: 0.4153 - precision_8: 0.5972 - recall_8: 0.5502 - val_accuracy: 0.8279 - val_loss: 0.3836 - val_precision_8: 0.6456 - val_recall_8: 0.5635
Epoch 21/100
[1m197/197[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 2ms/step - accuracy: 0.8246 - loss: 0.4133 - precision_8: 0.6430 - recall_8: 0.5762 - val_accuracy: 0.8273 - val_loss: 0.3826 - val_precision_8: 0.6454 - val_recall_8: 0.5580
Epoch 22/100
[1m197/197[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 2ms/step - accuracy: 0.8174 - loss: 0.4132 - precision_8: 0.6172 - recall_8: 0.5482 - val_accuracy: 0.8235 - val_loss: 0.3822 - val_precision_8: 0.6332 - val_recall_8: 0.5580
Epoch 23/100
[1m197/197[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 2ms/step - accuracy: 0.8304 - loss: 0.3997 - precision_8: 0.6312 - recall_8: 0.5784 - val_accuracy: 0.8260 - val_loss: 0.3798 - val_precision_8: 0.6431 - val_recall_8: 0.5525
Epoch 24/100
[1m197/197[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 2ms/step - accuracy: 0.8263 - loss: 0.4006 - precision_8: 0.6146 - recall_8: 0.5736 - val_accuracy: 0.8260 - val_loss: 0.3792 - val_precision_8: 0.6422 - val_recall_8: 0.5552
Epoch 25/100
[1m197/197[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 2ms/step - accuracy: 0.8150 - loss: 0.4198 - precision_8: 0.6177 - recall_8: 0.5467 - val_accuracy: 0.8266 - val_loss: 0.3778 - val_precision_8: 0.6433 - val_recall_8: 0.5580
Epoch 26/100
[1m197/197[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 2ms/step - accuracy: 0.8324 - loss: 0.3962 - precision_8: 0.6596 - recall_8: 0.5817 - val_accuracy: 0.8254 - val_loss: 0.3762 - val_precision_8: 0.6447 - val_recall_8: 0.5414
Epoch 27/100
[1m197/197[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 2ms/step - accuracy: 0.8223 - loss: 0.4004 - precision_8: 0.6243 - recall_8: 0.5655 - val_accuracy: 0.8260 - val_loss: 0.3761 - val_precision_8: 0.6478 - val_recall_8: 0.5387
Epoch 28/100
[1m197/197[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 2ms/step - accuracy: 0.8150 - loss: 0.4028 - precision_8: 0.6128 - recall_8: 0.5350 - val_accuracy: 0.8254 - val_loss: 0.3751 - val_precision_8: 0.6467 - val_recall_8: 0.5359
Epoch 29/100
[1m197/197[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 2ms/step - accuracy: 0.8247 - loss: 0.3945 - precision_8: 0.6104 - recall_8: 0.5702 - val_accuracy: 0.8247 - val_loss: 0.3748 - val_precision_8: 0.6417 - val_recall_8: 0.5442
Epoch 30/100
[1m197/197[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 2ms/step - accuracy: 0.8276 - loss: 0.3993 - precision_8: 0.6436 - recall_8: 0.5702 - val_accuracy: 0.8254 - val_loss: 0.3735 - val_precision_8: 0.6447 - val_recall_8: 0.5414
Epoch 31/100
[1m197/197[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 2ms/step - accuracy: 0.8179 - loss: 0.4020 - precision_8: 0.6109 - recall_8: 0.5423 - val_accuracy: 0.8254 - val_loss: 0.3737 - val_precision_8: 0.6438 - val_recall_8: 0.5442
Epoch 32/100
[1m197/197[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 2ms/step - accuracy: 0.8264 - loss: 0.3976 - precision_8: 0.6505 - recall_8: 0.5423 - val_accuracy: 0.8266 - val_loss: 0.3729 - val_precision_8: 0.6480 - val_recall_8: 0.5442
Epoch 33/100
[1m197/197[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 2ms/step - accuracy: 0.8268 - loss: 0.3921 - precision_8: 0.6214 - recall_8: 0.5360 - val_accuracy: 0.8260 - val_loss: 0.3721 - val_precision_8: 0.6469 - val_recall_8: 0.5414
Epoch 34/100
[1m197/197[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 2ms/step - accuracy: 0.8201 - loss: 0.4083 - precision_8: 0.6330 - recall_8: 0.5348 - val_accuracy: 0.8273 - val_loss: 0.3719 - val_precision_8: 0.6472 - val_recall_8: 0.5525
Epoch 35/100
[1m197/197[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 2ms/step - accuracy: 0.8250 - loss: 0.3812 - precision_8: 0.6311 - recall_8: 0.5414 - val_accuracy: 0.8260 - val_loss: 0.3720 - val_precision_8: 0.6469 - val_recall_8: 0.5414
Epoch 36/100
[1m197/197[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 2ms/step - accuracy: 0.8213 - loss: 0.3945 - precision_8: 0.6543 - recall_8: 0.5537 - val_accuracy: 0.8266 - val_loss: 0.3711 - val_precision_8: 0.6490 - val_recall_8: 0.5414
Epoch 37/100
[1m197/197[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 2ms/step - accuracy: 0.8162 - loss: 0.3973 - precision_8: 0.6009 - recall_8: 0.5178 - val_accuracy: 0.8260 - val_loss: 0.3707 - val_precision_8: 0.6478 - val_recall_8: 0.5387
Epoch 38/100
[1m197/197[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 2ms/step - accuracy: 0.8341 - loss: 0.3730 - precision_8: 0.6487 - recall_8: 0.5551 - val_accuracy: 0.8273 - val_loss: 0.3694 - val_precision_8: 0.6532 - val_recall_8: 0.5359
Epoch 39/100
[1m197/197[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 2ms/step - accuracy: 0.8152 - loss: 0.4005 - precision_8: 0.6271 - recall_8: 0.5190 - val_accuracy: 0.8286 - val_loss: 0.3686 - val_precision_8: 0.6545 - val_recall_8: 0.5442
Epoch 40/100
[1m197/197[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 2ms/step - accuracy: 0.8288 - loss: 0.3812 - precision_8: 0.6560 - recall_8: 0.5491 - val_accuracy: 0.8286 - val_loss: 0.3680 - val_precision_8: 0.6566 - val_recall_8: 0.5387
Epoch 41/100
[1m197/197[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 2ms/step - accuracy: 0.8353 - loss: 0.3813 - precision_8: 0.6570 - recall_8: 0.5684 - val_accuracy: 0.8292 - val_loss: 0.3684 - val_precision_8: 0.6546 - val_recall_8: 0.5497
Epoch 42/100
[1m197/197[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 2ms/step - accuracy: 0.8338 - loss: 0.3749 - precision_8: 0.6582 - recall_8: 0.5447 - val_accuracy: 0.8292 - val_loss: 0.3677 - val_precision_8: 0.6577 - val_recall_8: 0.5414
Epoch 43/100
[1m197/197[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 2ms/step - accuracy: 0.8391 - loss: 0.3620 - precision_8: 0.6683 - recall_8: 0.5683 - val_accuracy: 0.8286 - val_loss: 0.3674 - val_precision_8: 0.6555 - val_recall_8: 0.5414
Epoch 44/100
[1m197/197[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 2ms/step - accuracy: 0.8300 - loss: 0.3889 - precision_8: 0.6698 - recall_8: 0.5545 - val_accuracy: 0.8286 - val_loss: 0.3666 - val_precision_8: 0.6598 - val_recall_8: 0.5304
Epoch 45/100
[1m197/197[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 2ms/step - accuracy: 0.8373 - loss: 0.3791 - precision_8: 0.6659 - recall_8: 0.5561 - val_accuracy: 0.8292 - val_loss: 0.3675 - val_precision_8: 0.6567 - val_recall_8: 0.5442
Epoch 46/100
[1m197/197[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 2ms/step - accuracy: 0.8304 - loss: 0.3734 - precision_8: 0.6412 - recall_8: 0.5511 - val_accuracy: 0.8279 - val_loss: 0.3670 - val_precision_8: 0.6554 - val_recall_8: 0.5359
Epoch 47/100
[1m197/197[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 2ms/step - accuracy: 0.8289 - loss: 0.3765 - precision_8: 0.6545 - recall_8: 0.5446 - val_accuracy: 0.8286 - val_loss: 0.3668 - val_precision_8: 0.6566 - val_recall_8: 0.5387
Epoch 48/100
[1m197/197[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 2ms/step - accuracy: 0.8268 - loss: 0.3777 - precision_8: 0.6414 - recall_8: 0.5427 - val_accuracy: 0.8292 - val_loss: 0.3668 - val_precision_8: 0.6556 - val_recall_8: 0.5470
Epoch 49/100
[1m197/197[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 2ms/step - accuracy: 0.8322 - loss: 0.3775 - precision_8: 0.6419 - recall_8: 0.5529 - val_accuracy: 0.8305 - val_loss: 0.3664 - val_precision_8: 0.6600 - val_recall_8: 0.5470
Epoch 50/100
[1m197/197[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 2ms/step - accuracy: 0.8376 - loss: 0.3551 - precision_8: 0.6663 - recall_8: 0.5657 - val_accuracy: 0.8292 - val_loss: 0.3656 - val_precision_8: 0.6588 - val_recall_8: 0.5387
Epoch 51/100
[1m197/197[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 2ms/step - accuracy: 0.8400 - loss: 0.3705 - precision_8: 0.6705 - recall_8: 0.5815 - val_accuracy: 0.8317 - val_loss: 0.3665 - val_precision_8: 0.6678 - val_recall_8: 0.5387
Epoch 52/100
[1m197/197[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 2ms/step - accuracy: 0.8355 - loss: 0.3839 - precision_8: 0.6827 - recall_8: 0.5705 - val_accuracy: 0.8324 - val_loss: 0.3659 - val_precision_8: 0.6634 - val_recall_8: 0.5552
Epoch 53/100
[1m197/197[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 2ms/step - accuracy: 0.8387 - loss: 0.3595 - precision_8: 0.6568 - recall_8: 0.5742 - val_accuracy: 0.8324 - val_loss: 0.3656 - val_precision_8: 0.6678 - val_recall_8: 0.5442
Epoch 54/100
[1m197/197[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 2ms/step - accuracy: 0.8372 - loss: 0.3597 - precision_8: 0.6631 - recall_8: 0.5622 - val_accuracy: 0.8298 - val_loss: 0.3650 - val_precision_8: 0.6610 - val_recall_8: 0.5387
Epoch 55/100
[1m197/197[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 2ms/step - accuracy: 0.8391 - loss: 0.3741 - precision_8: 0.6598 - recall_8: 0.5796 - val_accuracy: 0.8311 - val_loss: 0.3655 - val_precision_8: 0.6644 - val_recall_8: 0.5414
Epoch 56/100
[1m197/197[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 2ms/step - accuracy: 0.8338 - loss: 0.3638 - precision_8: 0.6465 - recall_8: 0.5463 - val_accuracy: 0.8305 - val_loss: 0.3653 - val_precision_8: 0.6633 - val_recall_8: 0.5387
Epoch 57/100
[1m197/197[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 2ms/step - accuracy: 0.8314 - loss: 0.3737 - precision_8: 0.6488 - recall_8: 0.5412 - val_accuracy: 0.8286 - val_loss: 0.3654 - val_precision_8: 0.6555 - val_recall_8: 0.5414
Epoch 58/100
[1m197/197[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 2ms/step - accuracy: 0.8330 - loss: 0.3713 - precision_8: 0.6438 - recall_8: 0.5341 - val_accuracy: 0.8317 - val_loss: 0.3645 - val_precision_8: 0.6655 - val_recall_8: 0.5442
Epoch 59/100
[1m197/197[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 2ms/step - accuracy: 0.8323 - loss: 0.3741 - precision_8: 0.6759 - recall_8: 0.5399 - val_accuracy: 0.8311 - val_loss: 0.3643 - val_precision_8: 0.6644 - val_recall_8: 0.5414
Epoch 60/100
[1m197/197[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 2ms/step - accuracy: 0.8327 - loss: 0.3729 - precision_8: 0.6810 - recall_8: 0.5465 - val_accuracy: 0.8311 - val_loss: 0.3643 - val_precision_8: 0.6611 - val_recall_8: 0.5497
Epoch 61/100
[1m197/197[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 2ms/step - accuracy: 0.8317 - loss: 0.3612 - precision_8: 0.6674 - recall_8: 0.5431 - val_accuracy: 0.8324 - val_loss: 0.3643 - val_precision_8: 0.6656 - val_recall_8: 0.5497
Epoch 62/100
[1m197/197[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 2ms/step - accuracy: 0.8332 - loss: 0.3791 - precision_8: 0.6718 - recall_8: 0.5578 - val_accuracy: 0.8292 - val_loss: 0.3640 - val_precision_8: 0.6610 - val_recall_8: 0.5331
Epoch 63/100
[1m197/197[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 2ms/step - accuracy: 0.8334 - loss: 0.3673 - precision_8: 0.6604 - recall_8: 0.5489 - val_accuracy: 0.8324 - val_loss: 0.3641 - val_precision_8: 0.6701 - val_recall_8: 0.5387
Epoch 64/100
[1m197/197[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 2ms/step - accuracy: 0.8358 - loss: 0.3700 - precision_8: 0.6589 - recall_8: 0.5475 - val_accuracy: 0.8317 - val_loss: 0.3636 - val_precision_8: 0.6713 - val_recall_8: 0.5304
Epoch 65/100
[1m197/197[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 2ms/step - accuracy: 0.8305 - loss: 0.3731 - precision_8: 0.6292 - recall_8: 0.5202 - val_accuracy: 0.8324 - val_loss: 0.3635 - val_precision_8: 0.6749 - val_recall_8: 0.5276
Epoch 66/100
[1m197/197[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 2ms/step - accuracy: 0.8241 - loss: 0.3811 - precision_8: 0.6307 - recall_8: 0.5211 - val_accuracy: 0.8324 - val_loss: 0.3634 - val_precision_8: 0.6689 - val_recall_8: 0.5414
Epoch 67/100
[1m197/197[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 2ms/step - accuracy: 0.8265 - loss: 0.3739 - precision_8: 0.6553 - recall_8: 0.5377 - val_accuracy: 0.8317 - val_loss: 0.3640 - val_precision_8: 0.6612 - val_recall_8: 0.5552
Epoch 68/100
[1m197/197[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 2ms/step - accuracy: 0.8334 - loss: 0.3778 - precision_8: 0.6608 - recall_8: 0.5486 - val_accuracy: 0.8324 - val_loss: 0.3635 - val_precision_8: 0.6689 - val_recall_8: 0.5414
Epoch 69/100
[1m197/197[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 2ms/step - accuracy: 0.8376 - loss: 0.3636 - precision_8: 0.6713 - recall_8: 0.5580 - val_accuracy: 0.8298 - val_loss: 0.3630 - val_precision_8: 0.6655 - val_recall_8: 0.5276
Epoch 70/100
[1m197/197[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 2ms/step - accuracy: 0.8362 - loss: 0.3669 - precision_8: 0.6849 - recall_8: 0.5507 - val_accuracy: 0.8317 - val_loss: 0.3637 - val_precision_8: 0.6655 - val_recall_8: 0.5442
Epoch 71/100
[1m197/197[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 2ms/step - accuracy: 0.8334 - loss: 0.3640 - precision_8: 0.6593 - recall_8: 0.5502 - val_accuracy: 0.8324 - val_loss: 0.3629 - val_precision_8: 0.6689 - val_recall_8: 0.5414
Epoch 72/100
[1m197/197[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 2ms/step - accuracy: 0.8319 - loss: 0.3702 - precision_8: 0.6577 - recall_8: 0.5495 - val_accuracy: 0.8311 - val_loss: 0.3629 - val_precision_8: 0.6655 - val_recall_8: 0.5387
Epoch 73/100
[1m197/197[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 2ms/step - accuracy: 0.8420 - loss: 0.3638 - precision_8: 0.6788 - recall_8: 0.5723 - val_accuracy: 0.8311 - val_loss: 0.3627 - val_precision_8: 0.6633 - val_recall_8: 0.5442
Epoch 74/100
[1m197/197[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 2ms/step - accuracy: 0.8412 - loss: 0.3562 - precision_8: 0.6802 - recall_8: 0.5739 - val_accuracy: 0.8337 - val_loss: 0.3627 - val_precision_8: 0.6810 - val_recall_8: 0.5249
Epoch 75/100
[1m197/197[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 2ms/step - accuracy: 0.8274 - loss: 0.3683 - precision_8: 0.6650 - recall_8: 0.5381 - val_accuracy: 0.8317 - val_loss: 0.3630 - val_precision_8: 0.6655 - val_recall_8: 0.5442
Epoch 76/100
[1m197/197[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 2ms/step - accuracy: 0.8426 - loss: 0.3558 - precision_8: 0.6766 - recall_8: 0.5727 - val_accuracy: 0.8317 - val_loss: 0.3622 - val_precision_8: 0.6655 - val_recall_8: 0.5442
Epoch 77/100
[1m197/197[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 2ms/step - accuracy: 0.8356 - loss: 0.3642 - precision_8: 0.6529 - recall_8: 0.5354 - val_accuracy: 0.8330 - val_loss: 0.3621 - val_precision_8: 0.6786 - val_recall_8: 0.5249
Epoch 78/100
[1m197/197[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 2ms/step - accuracy: 0.8454 - loss: 0.3559 - precision_8: 0.6915 - recall_8: 0.5704 - val_accuracy: 0.8343 - val_loss: 0.3618 - val_precision_8: 0.6783 - val_recall_8: 0.5359
Epoch 79/100
[1m197/197[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 2ms/step - accuracy: 0.8261 - loss: 0.3791 - precision_8: 0.6638 - recall_8: 0.5373 - val_accuracy: 0.8330 - val_loss: 0.3616 - val_precision_8: 0.6701 - val_recall_8: 0.5442
Epoch 80/100
[1m197/197[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 2ms/step - accuracy: 0.8337 - loss: 0.3636 - precision_8: 0.6508 - recall_8: 0.5353 - val_accuracy: 0.8324 - val_loss: 0.3617 - val_precision_8: 0.6713 - val_recall_8: 0.5359
Epoch 81/100
[1m197/197[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 2ms/step - accuracy: 0.8293 - loss: 0.3675 - precision_8: 0.6453 - recall_8: 0.5406 - val_accuracy: 0.8324 - val_loss: 0.3621 - val_precision_8: 0.6689 - val_recall_8: 0.5414
Epoch 82/100
[1m197/197[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 2ms/step - accuracy: 0.8407 - loss: 0.3561 - precision_8: 0.6882 - recall_8: 0.5556 - val_accuracy: 0.8330 - val_loss: 0.3618 - val_precision_8: 0.6724 - val_recall_8: 0.5387
Epoch 83/100
[1m197/197[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 2ms/step - accuracy: 0.8322 - loss: 0.3643 - precision_8: 0.6743 - recall_8: 0.5441 - val_accuracy: 0.8330 - val_loss: 0.3611 - val_precision_8: 0.6724 - val_recall_8: 0.5387
Epoch 84/100
[1m197/197[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 2ms/step - accuracy: 0.8353 - loss: 0.3666 - precision_8: 0.6850 - recall_8: 0.5476 - val_accuracy: 0.8317 - val_loss: 0.3613 - val_precision_8: 0.6644 - val_recall_8: 0.5470
Epoch 85/100
[1m197/197[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 2ms/step - accuracy: 0.8315 - loss: 0.3651 - precision_8: 0.6574 - recall_8: 0.5457 - val_accuracy: 0.8324 - val_loss: 0.3608 - val_precision_8: 0.6725 - val_recall_8: 0.5331
Epoch 86/100
[1m197/197[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 2ms/step - accuracy: 0.8375 - loss: 0.3556 - precision_8: 0.6500 - recall_8: 0.5613 - val_accuracy: 0.8324 - val_loss: 0.3609 - val_precision_8: 0.6737 - val_recall_8: 0.5304
Epoch 87/100
[1m197/197[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 2ms/step - accuracy: 0.8382 - loss: 0.3612 - precision_8: 0.6660 - recall_8: 0.5324 - val_accuracy: 0.8330 - val_loss: 0.3611 - val_precision_8: 0.6786 - val_recall_8: 0.5249
Epoch 88/100
[1m197/197[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 2ms/step - accuracy: 0.8201 - loss: 0.3814 - precision_8: 0.6482 - recall_8: 0.5184 - val_accuracy: 0.8317 - val_loss: 0.3612 - val_precision_8: 0.6725 - val_recall_8: 0.5276
Epoch 89/100
[1m197/197[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 2ms/step - accuracy: 0.8368 - loss: 0.3592 - precision_8: 0.6620 - recall_8: 0.5497 - val_accuracy: 0.8330 - val_loss: 0.3613 - val_precision_8: 0.6773 - val_recall_8: 0.5276
Epoch 90/100
[1m197/197[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 2ms/step - accuracy: 0.8276 - loss: 0.3667 - precision_8: 0.6685 - recall_8: 0.5358 - val_accuracy: 0.8305 - val_loss: 0.3614 - val_precision_8: 0.6633 - val_recall_8: 0.5387
Epoch 91/100
[1m197/197[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 2ms/step - accuracy: 0.8292 - loss: 0.3667 - precision_8: 0.6584 - recall_8: 0.5177 - val_accuracy: 0.8324 - val_loss: 0.3611 - val_precision_8: 0.6713 - val_recall_8: 0.5359
Epoch 92/100
[1m197/197[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 2ms/step - accuracy: 0.8352 - loss: 0.3610 - precision_8: 0.6809 - recall_8: 0.5460 - val_accuracy: 0.8330 - val_loss: 0.3608 - val_precision_8: 0.6736 - val_recall_8: 0.5359
Epoch 93/100
[1m197/197[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 2ms/step - accuracy: 0.8353 - loss: 0.3686 - precision_8: 0.6952 - recall_8: 0.5419 - val_accuracy: 0.8311 - val_loss: 0.3614 - val_precision_8: 0.6738 - val_recall_8: 0.5193
Epoch 94/100
[1m197/197[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 2ms/step - accuracy: 0.8469 - loss: 0.3577 - precision_8: 0.7083 - recall_8: 0.5690 - val_accuracy: 0.8311 - val_loss: 0.3612 - val_precision_8: 0.6702 - val_recall_8: 0.5276
Epoch 95/100
[1m197/197[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 2ms/step - accuracy: 0.8320 - loss: 0.3733 - precision_8: 0.6772 - recall_8: 0.5305 - val_accuracy: 0.8305 - val_loss: 0.3609 - val_precision_8: 0.6667 - val_recall_8: 0.5304

# ========================
# Section 5: Evaluation and Visualization
# ========================
print("\nEvaluating final model...")

# Generate predictions
y_pred = (final_model.predict(X_test_preprocessed) > 0.5).astype("int32")
y_proba = final_model.predict(X_test_preprocessed)

# Evaluate performance
print("\n" + "="*50)
print(f"Best Architecture: {best_arch}")
print("="*50)
print("Classification Report:")
print(classification_report(y_test, y_pred))

# Visualize confusion matrix
from sklearn.metrics import ConfusionMatrixDisplay
plt.figure(figsize=(8, 6))
ConfusionMatrixDisplay.from_predictions(y_test, y_pred, cmap='Blues')
plt.title('Confusion Matrix')
plt.savefig('confusion_matrix.png')
plt.show()

print(f"ROC AUC: {roc_auc_score(y_test, y_proba):.4f}")

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
# Check if 'accuracy' or 'acc' is used
acc_key = 'accuracy' if 'accuracy' in history.history else 'acc'
val_acc_key = 'val_accuracy' if 'val_accuracy' in history.history else 'val_acc'

plt.plot(history.history[acc_key], label='Training Accuracy')
plt.plot(history.history[val_acc_key], label='Validation Accuracy')
plt.title('Training and Validation Accuracy')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend()

plt.tight_layout()
plt.savefig('training_history.png')
plt.show()


///output
Evaluating final model...
[1m50/50[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 1ms/step
[1m50/50[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 883us/step

==================================================
Best Architecture: (100,)
==================================================
Classification Report:
              precision    recall  f1-score   support

           0       0.87      0.92      0.89      1207
           1       0.67      0.53      0.59       362

    accuracy                           0.83      1569
   macro avg       0.77      0.73      0.74      1569
weighted avg       0.82      0.83      0.83      1569

