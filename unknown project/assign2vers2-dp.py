"""
CIFAR-10 Image Classification with PyTorch

This script trains a CNN on the CIFAR-10 dataset, testing different architectures
and hyperparameters to find the best model. It includes:

- Data loading and augmentation
- Multiple model architectures (including ResNet-style)
- Hyperparameter tuning
- Training with validation
- Performance evaluation
- Visualization of results

"""

# Standard imports
import numpy as np
import matplotlib.pyplot as plt
import time
import random
from sklearn.metrics import confusion_matrix, classification_report

# PyTorch imports
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from torchvision import datasets, transforms

# Set up reproducibility
def set_seeds(seed=42):
    """Set all random seeds for reproducibility"""
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False

set_seeds(42)

# Check GPU availability
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"Using device: {device}")

if torch.cuda.is_available():
    try:
        print(f"GPU: {torch.cuda.get_device_name(0)}")
        print(f"Memory: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB")
    except Exception as e:
        print(f"Couldn't get GPU details: {e}")

# Data Preparation ------------------------------------------------------------
print("\nLoading and preparing CIFAR-10 data...")

# Custom augmentation: Randomly shift RGB channels independently
class ChannelShift:
    """Adds small random shifts to each color channel"""
    def __init__(self, intensity=0.1):
        self.intensity = intensity
    
    def __call__(self, img):
        shifts = torch.randn(3) * self.intensity
        shifted_img = img.clone()
        for c in range(3):
            shifted_img[c] = torch.clamp(img[c] + shifts[c], -1, 1)
        return shifted_img

# Training transforms with augmentation
train_transform = transforms.Compose([
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(15),
    transforms.ColorJitter(brightness=0.2, contrast=0.2),
    transforms.ToTensor(),
    ChannelShift(intensity=0.15),
    transforms.RandomErasing(p=0.2)
])

# Simple transform for test data
test_transform = transforms.Compose([
    transforms.ToTensor(),
])

# Load datasets
train_dataset = datasets.CIFAR10(root='./data', train=True, download=True, transform=train_transform)
test_dataset = datasets.CIFAR10(root='./data', train=False, download=True, transform=test_transform)

# Convert to numpy for analysis
x_train = train_dataset.data
y_train = np.array(train_dataset.targets)
x_test = test_dataset.data
y_test = np.array(test_dataset.targets)

# Normalize data to [-1, 1] range (better for CNNs)
print("Normalizing data to [-1, 1] range...")
x_train = (x_train.astype('float32') - 127.5) / 127.5
x_test = (x_test.astype('float32') - 127.5) / 127.5

# Class names for reference
class_names = ['airplane', 'automobile', 'bird', 'cat', 'deer',
               'dog', 'frog', 'horse', 'ship', 'truck']

# Show sample images
def show_samples(images, labels, n=25):
    """Display a grid of sample images"""
    plt.figure(figsize=(10,10))
    for i in range(n):
        plt.subplot(5,5,i+1)
        plt.imshow((images[i] + 1)/2)  # Convert back to [0,1] for display
        plt.title(class_names[labels[i]])
        plt.axis('off')
    plt.tight_layout()
    plt.show()

print("\nSample training images:")
show_samples(x_train, y_train)

# Model Definitions -----------------------------------------------------------

class BasicBlock(nn.Module):
    """A simple residual block for our CNN"""
    def __init__(self, in_channels, out_channels, stride=1):
        super().__init__()
        self.conv1 = nn.Conv2d(in_channels, out_channels, kernel_size=3, 
                              stride=stride, padding=1, bias=False)
        self.bn1 = nn.BatchNorm2d(out_channels)
        self.conv2 = nn.Conv2d(out_channels, out_channels, kernel_size=3,
                              stride=1, padding=1, bias=False)
        self.bn2 = nn.BatchNorm2d(out_channels)
        
        # Shortcut connection if dimensions change
        self.shortcut = nn.Sequential()
        if stride != 1 or in_channels != out_channels:
            self.shortcut = nn.Sequential(
                nn.Conv2d(in_channels, out_channels, kernel_size=1, 
                          stride=stride, bias=False),
                nn.BatchNorm2d(out_channels)
            )
    
    def forward(self, x):
        out = F.relu(self.bn1(self.conv1(x)))
        out = self.bn2(self.conv2(out))
        out += self.shortcut(x)
        return F.relu(out)

class CIFAR10_CNN(nn.Module):
    """Our main CNN model for CIFAR-10 classification"""
    def __init__(self, num_blocks=[2,2,2], num_classes=10, dropout_rate=0.3):
        super().__init__()
        self.in_channels = 64
        
        # Initial convolution
        self.conv1 = nn.Conv2d(3, 64, kernel_size=3, stride=1, padding=1, bias=False)
        self.bn1 = nn.BatchNorm2d(64)
        
        # Residual blocks
        self.layer1 = self._make_layer(64, num_blocks[0], stride=1)
        self.layer2 = self._make_layer(128, num_blocks[1], stride=2)
        self.layer3 = self._make_layer(256, num_blocks[2], stride=2)
        
        # Classifier
        self.avg_pool = nn.AdaptiveAvgPool2d(1)
        self.fc = nn.Linear(256, num_classes)
        self.dropout = nn.Dropout(dropout_rate)
    
    def _make_layer(self, out_channels, num_blocks, stride):
        """Helper to create residual blocks"""
        strides = [stride] + [1]*(num_blocks-1)
        layers = []
        for stride in strides:
            layers.append(BasicBlock(self.in_channels, out_channels, stride))
            self.in_channels = out_channels
        return nn.Sequential(*layers)
    
    def forward(self, x):
        x = F.relu(self.bn1(self.conv1(x)))
        
        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        
        x = self.avg_pool(x)
        x = x.view(x.size(0), -1)
        x = self.dropout(x)
        x = self.fc(x)
        return x

# Training Setup --------------------------------------------------------------

def create_dataloaders(batch_size=128):
    """Create train, validation, and test dataloaders"""
    # Split train into train/validation
    x_train_tensor = torch.FloatTensor(x_train).permute(0, 3, 1, 2)  # NHWC to NCHW
    y_train_tensor = torch.LongTensor(y_train)
    
    # Use 80/20 split
    train_size = int(0.8 * len(x_train_tensor))
    val_size = len(x_train_tensor) - train_size
    
    train_dataset = TensorDataset(x_train_tensor[:train_size], y_train_tensor[:train_size])
    val_dataset = TensorDataset(x_train_tensor[train_size:], y_train_tensor[train_size:])
    
    # Test data
    x_test_tensor = torch.FloatTensor(x_test).permute(0, 3, 1, 2)
    y_test_tensor = torch.LongTensor(y_test)
    test_dataset = TensorDataset(x_test_tensor, y_test_tensor)
    
    # Create dataloaders
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)
    
    return train_loader, val_loader, test_loader

# Training Functions ----------------------------------------------------------

def train_epoch(model, loader, criterion, optimizer, device):
    """Train for one epoch"""
    model.train()
    running_loss = 0.0
    correct = 0
    total = 0
    
    for inputs, labels in loader:
        inputs, labels = inputs.to(device), labels.to(device)
        
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        
        running_loss += loss.item()
        _, predicted = outputs.max(1)
        total += labels.size(0)
        correct += predicted.eq(labels).sum().item()
    
    epoch_loss = running_loss / len(loader)
    epoch_acc = 100. * correct / total
    return epoch_loss, epoch_acc

def validate(model, loader, criterion, device):
    """Evaluate on validation set"""
    model.eval()
    running_loss = 0.0
    correct = 0
    total = 0
    
    with torch.no_grad():
        for inputs, labels in loader:
            inputs, labels = inputs.to(device), labels.to(device)
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            
            running_loss += loss.item()
            _, predicted = outputs.max(1)
            total += labels.size(0)
            correct += predicted.eq(labels).sum().item()
    
    val_loss = running_loss / len(loader)
    val_acc = 100. * correct / total
    return val_loss, val_acc

def train_model(model, train_loader, val_loader, epochs=50, lr=0.001):
    """Main training loop"""
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.AdamW(model.parameters(), lr=lr, weight_decay=1e-4)
    scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, 'max', patience=5, factor=0.5)
    
    best_acc = 0.0
    history = {'train_loss': [], 'train_acc': [], 'val_loss': [], 'val_acc': []}
    
    print(f"\nTraining model for {epochs} epochs...")
    for epoch in range(epochs):
        train_loss, train_acc = train_epoch(model, train_loader, criterion, optimizer, device)
        val_loss, val_acc = validate(model, val_loader, criterion, device)
        
        # Update learning rate
        scheduler.step(val_acc)
        
        # Save best model
        if val_acc > best_acc:
            best_acc = val_acc
            torch.save(model.state_dict(), 'best_model.pth')
        
        # Record history
        history['train_loss'].append(train_loss)
        history['train_acc'].append(train_acc)
        history['val_loss'].append(val_loss)
        history['val_acc'].append(val_acc)
        
        # Print progress
        if (epoch + 1) % 5 == 0:
            print(f"Epoch {epoch+1}/{epochs}:")
            print(f"  Train Loss: {train_loss:.4f}, Acc: {train_acc:.2f}%")
            print(f"  Val Loss: {val_loss:.4f}, Acc: {val_acc:.2f}%")
    
    print(f"\nTraining complete! Best validation accuracy: {best_acc:.2f}%")
    return history

# Evaluation ------------------------------------------------------------------

def evaluate_model(model, test_loader):
    """Evaluate model on test set"""
    criterion = nn.CrossEntropyLoss()
    test_loss, test_acc = validate(model, test_loader, criterion, device)
    print(f"\nTest Accuracy: {test_acc:.2f}%")
    
    # Get all predictions
    all_preds = []
    all_labels = []
    with torch.no_grad():
        for inputs, labels in test_loader:
            inputs = inputs.to(device)
            outputs = model(inputs)
            _, preds = torch.max(outputs, 1)
            all_preds.extend(preds.cpu().numpy())
            all_labels.extend(labels.numpy())
    
    # Classification report
    print("\nClassification Report:")
    print(classification_report(all_labels, all_preds, target_names=class_names))
    
    # Confusion matrix
    cm = confusion_matrix(all_labels, all_preds)
    plt.figure(figsize=(10,8))
    plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
    plt.title('Confusion Matrix')
    plt.colorbar()
    tick_marks = np.arange(len(class_names))
    plt.xticks(tick_marks, class_names, rotation=45)
    plt.yticks(tick_marks, class_names)
    
    # Add text annotations
    thresh = cm.max() / 2.
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            plt.text(j, i, format(cm[i, j], 'd'),
                    ha="center", va="center",
                    color="white" if cm[i, j] > thresh else "black")
    
    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.show()

# Main Execution --------------------------------------------------------------

if __name__ == "__main__":
    # Create dataloaders
    train_loader, val_loader, test_loader = create_dataloaders(batch_size=128)
    
    # Initialize model
    model = CIFAR10_CNN(num_blocks=[2,2,2]).to(device)
    print(f"\nModel architecture:")
    print(model)
    
    # Train model
    history = train_model(model, train_loader, val_loader, epochs=50, lr=0.001)
    
    # Load best model and evaluate
    model.load_state_dict(torch.load('best_model.pth'))
    evaluate_model(model, test_loader)
    
    # Plot training history
    plt.figure(figsize=(12,4))
    plt.subplot(1,2,1)
    plt.plot(history['train_loss'], label='Train')
    plt.plot(history['val_loss'], label='Validation')
    plt.title('Loss over Epochs')
    plt.legend()
    
    plt.subplot(1,2,2)
    plt.plot(history['train_acc'], label='Train')
    plt.plot(history['val_acc'], label='Validation')
    plt.title('Accuracy over Epochs')
    plt.legend()
    plt.tight_layout()
    plt.show()