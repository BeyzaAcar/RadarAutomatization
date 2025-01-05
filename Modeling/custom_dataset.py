# custom_dataset.py

import os
import pandas as pd
from torch.utils.data import Dataset
from PIL import Image
import torch

class CustomSequenceDataset(Dataset):
    def __init__(self, csv_path, split, transform=None):
        self.data = pd.read_csv(csv_path)                       # CSV'yi oku
        self.data = self.data[self.data['Split'] == split]      # İlgili split (train/val/test) filtrele
        self.transform = transform

        # Label stringlerini sayısal değere dönüştürmek için label2idx
        self.unique_labels = sorted(self.data['Label'].unique())
        self.label2idx = {label: idx for idx, label in enumerate(self.unique_labels)}

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        trial_path = self.data.iloc[idx]['TrialPath']
        label_str  = self.data.iloc[idx]['Label']

        label_idx  = self.label2idx[label_str]            # String etiketi sayısal etiket
        label_tensor = torch.tensor(label_idx, dtype=torch.long)

        # Tüm frameleri yükle
        frames = []
        # sorted(...) ile frame_0, frame_1, frame_2 sıralı gelsin
        for frame_name in sorted(os.listdir(trial_path)):
            frame_path = os.path.join(trial_path, frame_name)
            if not frame_path.lower().endswith(('.jpg', '.png')):
                continue  # Resim olmayan dosyaları es geç

            image = Image.open(frame_path).convert('RGB')
            if self.transform:
                image = self.transform(image)
            frames.append(image)

        # frames: list of 3D tensors [C, H, W]
        # frames_tensor: shape (N, C, H, W)
        frames_tensor = torch.stack(frames)

        return frames_tensor, label_tensor

