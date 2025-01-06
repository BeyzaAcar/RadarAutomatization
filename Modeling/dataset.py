import os
import pandas as pd
from torch.utils.data import Dataset
from PIL import Image
import torch

class CameraFramesDataset(Dataset):
    def __init__(self, csv_path, split, transform=None):
        """
        Dataset sınıfı:
        - CSV'deki path'lere göre veri yükler
        - Train, val veya test verilerini seçer
        """
        self.data = pd.read_csv(csv_path, sep=';')
        self.data = self.data[self.data['Split'] == split]  # Train/Val/Test'e göre filtrele
        self.transform = transform

        # Label-to-Class dönüşümü
        self.label_to_class = {label: idx for idx, label in enumerate(self.data["Label"].unique())}
        self.data["Class"] = self.data["Label"].map(self.label_to_class)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        row = self.data.iloc[idx]
        trial_path = row["TrialPath"]
        label = row["Class"]

        # İlk frame'i yükle (örnek olarak)
        frame_names = sorted(os.listdir(trial_path))
        frame_path = os.path.join(trial_path, frame_names[0])  # Sadece ilk frame
        image = Image.open(frame_path).convert("RGB")
        if self.transform:
            image = self.transform(image)

        return image, label
