# ========================
# CIFAR-10 CNN with PyTorch - GPU Accelerated
# ========================
import numpy as np
import matplotlib.pyplot as plt
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from torch.utils.data import DataLoader, TensorDataset
from torchvision import datasets, transforms
import random
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score
from sklearn.model_selection import train_test_split
import time

# ========================
# Reproducibility Setup
# ========================
random.seed(42)
np.random.seed(42)
torch.manual_seed(42)
torch.cuda.manual_seed(42)
torch.backends.cudnn.deterministic = True

# ========================
# GPU Setup
# ========================
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"Using device: {device}")
if torch.cuda.is_available():
    print(f"GPU: {torch.cuda.get_device_name(0)}")
    print(f"CUDA version: {torch.version.cuda}")
    gpu_memory = torch.cuda.get_device_properties(0).total_memory / 1024**3
    print(f"GPU memory: {gpu_memory:.1f} GB")

# ========================
# Data Loading
# ========================
print("Loading CIFAR-10 data...")

# Simple transforms
train_transform = transforms.Compose([
    transforms.RandomHorizontalFlip(p=0.5),
    transforms.ToTensor(),
    transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
])

test_transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
])

# Load datasets
train_dataset = datasets.CIFAR10(root='./data', train=True, download=True, transform=train_transform)
test_dataset = datasets.CIFAR10(root='./data', train=False, download=True, transform=test_transform)

# Convert to numpy for analysis
x_train = train_dataset.data
y_train = np.array(train_dataset.targets)
x_test = test_dataset.data
y_test = np.array(test_dataset.targets)

# Normalize to [-1, 1]
x_train = (x_train.astype('float32') - 127.5) / 127.5
x_test = (x_test.astype('float32') - 127.5) / 127.5

print(f"Training samples: {x_train.shape[0]}")
print(f"Test samples: {x_test.shape[0]}")
print(f"Image shape: {x_train.shape[1:]}")

# Class names
class_names = ['airplane', 'automobile', 'bird', 'cat', 'deer',
               'dog', 'frog', 'horse', 'ship', 'truck']

# Convert to PyTorch tensors
x_train_tensor = torch.FloatTensor(x_train).permute(0, 3, 1, 2)
x_test_tensor = torch.FloatTensor(x_test).permute(0, 3, 1, 2)
y_train_tensor = torch.LongTensor(y_train)
y_test_tensor = torch.LongTensor(y_test)

# ========================
# Model Definition
# ========================
class SimpleCNN(nn.Module):
    def __init__(self, num_classes=10):
        super(SimpleCNN, self).__init__()
        
        self.features = nn.Sequential(
            # First conv block
            nn.Conv2d(3, 32, 3, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2),
            nn.Dropout2d(0.3),
            
            # Second conv block
            nn.Conv2d(32, 64, 3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2),
            nn.Dropout2d(0.3),
            
            # Third conv block
            nn.Conv2d(64, 128, 3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2),
            nn.Dropout2d(0.3),
        )
        
        self.classifier = nn.Sequential(
            nn.AdaptiveAvgPool2d(1),
            nn.Flatten(),
            nn.Linear(128, 256),
            nn.BatchNorm1d(256),
            nn.ReLU(inplace=True),
            nn.Dropout(0.5),
            nn.Linear(256, num_classes)
        )
    
    def forward(self, x):
        x = self.features(x)
        x = self.classifier(x)
        return x

# ========================
# Training Functions
# ========================
def train_epoch(model, dataloader, criterion, optimizer, device):
    model.train()
    running_loss = 0.0
    correct = 0
    total = 0
    
    for data, target in dataloader:
        data, target = data.to(device), target.to(device)
        
        optimizer.zero_grad()
        output = model(data)
        loss = criterion(output, target)
        loss.backward()
        optimizer.step()
        
        running_loss += loss.item()
        _, predicted = output.max(1)
        total += target.size(0)
        correct += predicted.eq(target).sum().item()
    
    epoch_loss = running_loss / len(dataloader)
    epoch_acc = 100. * correct / total
    return epoch_loss, epoch_acc

def validate_epoch(model, dataloader, criterion, device):
    model.eval()
    running_loss = 0.0
    correct = 0
    total = 0
    
    with torch.no_grad():
        for data, target in dataloader:
            data, target = data.to(device), target.to(device)
            output = model(data)
            loss = criterion(output, target)
            
            running_loss += loss.item()
            _, predicted = output.max(1)
            total += target.size(0)
            correct += predicted.eq(target).sum().item()
    
    epoch_loss = running_loss / len(dataloader)
    epoch_acc = 100. * correct / total
    return epoch_loss, epoch_acc

# ========================
# Training Setup
# ========================
print("Setting up training...")

# Create train/validation split
x_train_split, x_val_split, y_train_split, y_val_split = train_test_split(
    x_train_tensor, y_train_tensor, test_size=0.2, random_state=42, stratify=y_train_tensor
)

# Create dataloaders
batch_size = 128
train_loader = DataLoader(TensorDataset(x_train_split, y_train_split), 
                         batch_size=batch_size, shuffle=True, num_workers=2)
val_loader = DataLoader(TensorDataset(x_val_split, y_val_split), 
                       batch_size=batch_size, shuffle=False, num_workers=2)

# Model, loss, optimizer
model = SimpleCNN(num_classes=10).to(device)
criterion = nn.CrossEntropyLoss()
optimizer = optim.AdamW(model.parameters(), lr=0.0001, weight_decay=0.001)

print(f"Model created and moved to {device}")
print(f"Total parameters: {sum(p.numel() for p in model.parameters()):,}")

# ========================
# Training Loop
# ========================
print("Starting training...")
num_epochs = 50
best_val_acc = -1
patience_counter = 0
max_patience = 15

for epoch in range(num_epochs):
    # Train
    train_loss, train_acc = train_epoch(model, train_loader, criterion, optimizer, device)
    
    # Validate
    val_loss, val_acc = validate_epoch(model, val_loader, criterion, device)
    
    # Learning rate reduction
    if val_loss > best_val_acc:
        patience_counter += 1
        if patience_counter >= 8:
            for param_group in optimizer.param_groups:
                param_group['lr'] *= 0.2
            patience_counter = 0
            print(f"Epoch {epoch}: Reducing learning rate to {param_group['lr']:.2e}")
    else:
        patience_counter = 0
    
    # Early stopping
    if val_acc > best_val_acc:
        best_val_acc = val_acc
        best_weights = model.state_dict().copy()
    
    if patience_counter >= max_patience:
        print(f"Early stopping at epoch {epoch}")
        break
    
    if epoch % 5 == 0:
        print(f"Epoch {epoch}: Train Loss: {train_loss:.4f}, Train Acc: {train_acc:.2f}%, "
              f"Val Loss: {val_loss:.4f}, Val Acc: {val_acc:.2f}%")

print(f"Best validation accuracy: {best_val_acc:.4f}")

# Load best weights
model.load_state_dict(best_weights)

# ========================
# Final Evaluation
# ========================
print("Evaluating final model...")

# Create test dataloader
test_loader = DataLoader(TensorDataset(x_test_tensor, y_test_tensor), 
                        batch_size=batch_size, shuffle=False, num_workers=2)

# Evaluate on test set
model.eval()
test_loss, test_acc = validate_epoch(model, test_loader, criterion, device)
print(f"Final test accuracy: {test_acc:.4f}%")

# Detailed evaluation
print("Detailed evaluation...")
all_predictions = []
all_targets = []

with torch.no_grad():
    for data, target in test_loader:
        data, target = data.to(device), target.to(device)
        output = model(data)
        _, predicted = output.max(1)
        
        all_predictions.extend(predicted.cpu().numpy())
        all_targets.extend(target.cpu().numpy())

# Convert to numpy arrays
all_predictions = np.array(all_predictions)
all_targets = np.array(all_targets)

# Calculate overall accuracy
overall_accuracy = accuracy_score(all_targets, all_predictions)
print(f"Overall test accuracy: {overall_accuracy:.4f}")

# Confusion matrix
print("Confusion Matrix:")
cm = confusion_matrix(all_targets, all_predictions)
print(cm)

# Classification report
print("Classification Report:")
print(classification_report(all_targets, all_predictions, target_names=class_names))

# Per-class accuracy
print("Per-class accuracy:")
for class_idx in range(len(class_names)):
    class_mask = all_targets == class_idx
    if np.sum(class_mask) > 0:
        class_acc = accuracy_score(all_targets[class_mask], all_predictions[class_mask])
        print(f"  {class_names[class_idx]}: {class_acc:.4f}")

# Save model
torch.save({
    'model_state_dict': model.state_dict(),
    'test_accuracy': overall_accuracy,
    'class_names': class_names
}, 'cifar10_model_pytorch.pth')

print("Model saved to 'cifar10_model_pytorch.pth'")
print("Training complete!")
