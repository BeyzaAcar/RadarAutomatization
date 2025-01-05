# test.py

import torch
import torch.nn as nn
from torch.utils.data import DataLoader
import torchvision.transforms as transforms
import torchvision.models as models

from custom_dataset import CustomSequenceDataset

def main():
    test_transforms = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406],
                             std=[0.229, 0.224, 0.225])
    ])

    test_dataset = CustomSequenceDataset(
        csv_path="dataset.csv",
        split="test",
        transform=test_transforms
    )
    test_loader = DataLoader(test_dataset, batch_size=2, shuffle=False)

    num_classes = len(test_dataset.label2idx)

    # Modeli yükle
    model = models.resnet50(pretrained=True)
    in_features = model.fc.in_features
    model.fc = nn.Linear(in_features, num_classes)

    model.load_state_dict(torch.load("model_weights.pth"))
    model.eval()

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model.to(device)

    criterion = nn.CrossEntropyLoss()

    test_loss, test_correct = 0.0, 0
    total_samples = 0

    with torch.no_grad():
        for frames, labels in test_loader:
            frames = frames.to(device)
            labels = labels.to(device)

            b, n, c, h, w = frames.shape
            frames_reshaped = frames.view(b*n, c, h, w)

            outputs = model(frames_reshaped)
            labels_expanded = labels.unsqueeze(1).repeat(1, n).view(-1)

            loss = criterion(outputs, labels_expanded)
            test_loss += loss.item() * (b*n)

            _, preds = torch.max(outputs, 1)
            test_correct += torch.sum(preds == labels_expanded).item()
            total_samples += (b*n)

    avg_loss = test_loss / total_samples
    avg_acc = test_correct / total_samples
    print(f"Test Loss: {avg_loss:.4f}, Test Acc: {avg_acc:.4f}")

if __name__ == "__main__":
    main()
