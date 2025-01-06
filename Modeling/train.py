import torch
from torch.utils.data import DataLoader
from torchvision import transforms
from dataset import CameraFramesDataset
from model import get_model
import torch.nn as nn
import torch.optim as optim

# Dataset ve DataLoader
csv_path = "/content/drive/MyDrive/Dataset/dataset.csv"
train_transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

train_dataset = CameraFramesDataset(csv_path=csv_path, split="train", transform=train_transform)
val_dataset = CameraFramesDataset(csv_path=csv_path, split="val", transform=train_transform)

train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=32, shuffle=False)

# Model
num_classes = len(train_dataset.label_to_class)  # Sınıf sayısı
model = get_model(num_classes=num_classes)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device)

# Loss ve optimizer
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.0001)

# Eğitim döngüsü
num_epochs = 10
for epoch in range(num_epochs):
    # === Eğitim ===
    model.train()
    running_loss, running_corrects = 0.0, 0
    for inputs, labels in train_loader:
        inputs, labels = inputs.to(device), labels.to(device)

        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        running_loss += loss.item() * inputs.size(0)
        running_corrects += (outputs.argmax(1) == labels).sum().item()

    epoch_loss = running_loss / len(train_dataset)
    epoch_acc = running_corrects / len(train_dataset)
    print(f"Epoch {epoch+1}/{num_epochs}, Loss: {epoch_loss:.4f}, Acc: {epoch_acc:.4f}")

    # === Doğrulama ===
    model.eval()
    val_loss, val_corrects = 0.0, 0
    with torch.no_grad():
        for inputs, labels in val_loader:
            inputs, labels = inputs.to(device), labels.to(device)
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            val_loss += loss.item() * inputs.size(0)
            val_corrects += (outputs.argmax(1) == labels).sum().item()

    val_loss = val_loss / len(val_dataset)
    val_acc = val_corrects / len(val_dataset)
    print(f"Validation Loss: {val_loss:.4f}, Validation Acc: {val_acc:.4f}")
