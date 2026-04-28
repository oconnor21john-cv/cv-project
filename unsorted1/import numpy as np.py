import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import accuracy_score, roc_auc_score
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import SGD
from tensorflow.keras.callbacks import EarlyStopping

# Load data
data = pd.read_csv('as1-bank.csv')
print(f"Original data shape: {data.shape}")

# Convert target variable to binary (0/1)
label_encoder = LabelEncoder()
data['y'] = label_encoder.fit_transform(data['y'])

# Separate features and target
X = data.drop('y', axis=1)
y = data['y']

# Split data into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Standardize features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Function to create and train the model
def create_train_model(hidden_layers, units_per_layer, dropout_rate=0.3, epochs=100, patience=10):
    model = Sequential()
    model.add(Dense(units_per_layer, activation='relu', input_shape=(X_train_scaled.shape[1],)))
    model.add(Dropout(dropout_rate))
    
    for _ in range(hidden_layers - 1):
        model.add(Dense(units_per_layer, activation='relu'))
        model.add(Dropout(dropout_rate))
    
    model.add(Dense(1, activation='sigmoid'))
    
    sgd = SGD(learning_rate=0.01)
    model.compile(optimizer=sgd, loss='binary_crossentropy', metrics=['accuracy'])
    
    early_stopping = EarlyStopping(monitor='val_loss', patience=patience, restore_best_weights=True)
    history = model.fit(
        X_train_scaled, y_train,
        epochs=epochs,
        batch_size=32,
        validation_split=0.1,
        callbacks=[early_stopping],
        verbose=0
    )
    return model, history

# Experiment with different architectures
architectures = [
    (1, 64),   # 1 hidden layer, 64 units
    (2, 64),   # 2 hidden layers, 64 units each
    (3, 64),   # 3 hidden layers, 64 units each
    (1, 128),  # 1 hidden layer, 128 units
    (2, 128),  # 2 hidden layers, 128 units each
]

best_auc = 0
best_model = None
best_arch = None

for layers, units in architectures:
    print(f"\nTraining model: {layers} hidden layer(s), {units} units per layer")
    model, history = create_train_model(hidden_layers=layers, units_per_layer=units)
    
    # Predict probabilities for test set
    y_pred_proba = model.predict(X_test_scaled, verbose=0).flatten()
    auc = roc_auc_score(y_test, y_pred_proba)
    print(f"Test AUC: {auc:.4f}")
    
    if auc > best_auc:
        best_auc = auc
        best_model = model
        best_arch = (layers, units)

# Evaluate the best model
y_pred = (best_model.predict(X_test_scaled, verbose=0).flatten() > 0.5).astype(int)
accuracy = accuracy_score(y_test, y_pred)
print(f"\nBest Architecture: {best_arch[0]} hidden layers, {best_arch[1]} units per layer")
print(f"Final Test Accuracy: {accuracy:.4f}")
print(f"Final Test AUC: {best_auc:.4f}")

# Output best model summary
print("\nBest Model Summary:")
best_model.summary()