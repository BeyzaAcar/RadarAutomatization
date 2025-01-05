# train.py

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
import torchvision.transforms as transforms
import torchvision.models as models

from custom_dataset import CustomSequenceDataset

def main():
    # 1) Dataset & DataLoader
    train_transforms = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406],
                             std=[0.229, 0.224, 0.225])
    ])

    val_transforms = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406],
                             std=[0.229, 0.224, 0.225])
    ])

    train_dataset = CustomSequenceDataset(
        csv_path="dataset.csv",
        split="train",
        transform=train_transforms
    )
    val_dataset = CustomSequenceDataset(
        csv_path="dataset.csv",
        split="val",
        transform=val_transforms
    )

    train_loader = DataLoader(train_dataset, batch_size=2, shuffle=True)
    val_loader   = DataLoader(val_dataset,   batch_size=2, shuffle=False)

    num_classes = len(train_dataset.label2idx)  # Kaç farklı kişi var

    # 2) Model Kurulumu
    base_model = models.resnet50(pretrained=True)
    in_features = base_model.fc.in_features
    base_model.fc = nn.Linear(in_features, num_classes)

    # 3) GPU Kontrolü
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    base_model.to(device)

    # 4) Loss ve Optimizer
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(base_model.parameters(), lr=1e-4)

    # 5) Eğitim Döngüsü
    num_epochs = 5
    for epoch in range(num_epochs):
        # === EĞİTİM ===
        base_model.train()
        running_loss, running_correct = 0.0, 0
        for frames, labels in train_loader:
            # frames.shape = (batch_size, N, C, H, W)
            # Ancak ResNet'e (N, C, H, W) boyutu ile beslememiz gerekiyor
            # Yani (batch_size*N, C, H, W) olacak

            frames = frames.to(device)
            labels = labels.to(device)

            b, n, c, h, w = frames.shape
            frames_reshaped = frames.view(b*n, c, h, w)  # Hepsini arka arkaya

            optimizer.zero_grad()
            outputs = base_model(frames_reshaped)
            
            # outputs.shape = (batch_size*N, num_classes)
            # Bizde batch_size*N örnek var, label sayısı ise batch_size
            # AMA labels boyutu sadece (batch_size) => Her sample bir "tekrar" ise,
            # Normalde "tekrarın" hepsine aynı label gelecek.
            # Dolayısıyla labels'i tekrarlamamız lazım => (N kere)
            labels_expanded = labels.unsqueeze(1).repeat(1, n).view(-1)

            loss = criterion(outputs, labels_expanded)
            loss.backward()
            optimizer.step()

            running_loss += loss.item() * (b*n)
            _, preds = torch.max(outputs, 1)
            running_correct += torch.sum(preds == labels_expanded).item()

        epoch_loss = running_loss / len(train_dataset)  # Toplam sample sayısı
        epoch_acc = running_correct / len(train_dataset)

        # === DOĞRULAMA ===
        base_model.eval()
        val_loss, val_correct = 0.0, 0
        with torch.no_grad():
            for frames, labels in val_loader:
                frames = frames.to(device)
                labels = labels.to(device)

                b, n, c, h, w = frames.shape
                frames_reshaped = frames.view(b*n, c, h, w)

                outputs = base_model(frames_reshaped)
                labels_expanded = labels.unsqueeze(1).repeat(1, n).view(-1)

                loss = criterion(outputs, labels_expanded)
                val_loss += loss.item() * (b*n)

                _, preds = torch.max(outputs, 1)
                val_correct += torch.sum(preds == labels_expanded).item()

        val_loss = val_loss / len(val_dataset)
        val_acc = val_correct / len(val_dataset)

        print(f"Epoch [{epoch+1}/{num_epochs}] "
              f"Train Loss: {epoch_loss:.4f}, Train Acc: {epoch_acc:.4f} | "
              f"Val Loss: {val_loss:.4f}, Val Acc: {val_acc:.4f}")

    # 6) Modeli Kaydet
    torch.save(base_model.state_dict(), "model_weights.pth")
    print("Eğitim tamamlandı ve model_weights.pth kaydedildi.")

if __name__ == "__main__":
    main()
