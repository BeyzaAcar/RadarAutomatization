import os
import pandas as pd
import random

# Ana veri klasörünüz
root_dir = "C:/Users/user/Desktop/RADAR_PROJECT/Dataset/LabelledDataset"  # Tüm kişilerin olduğu ana klasör
splits = ['train', 'val', 'test']
split_ratios = [0.7, 0.2, 0.1]  # Eğitim, doğrulama, test oranları

data = []

for person in os.listdir(root_dir):
    person_path = os.path.join(root_dir, person, "CameraFrames")
    if os.path.isdir(person_path):
        # Kişinin tekrar klasörlerini topla
        trials = [os.path.join(person_path, trial) for trial in os.listdir(person_path) if os.path.isdir(os.path.join(person_path, trial))]
        random.shuffle(trials)  # Tekrarları karıştır

        num_trials = len(trials)
        if num_trials >= 4:  # Normal ayırma
            num_train = int(num_trials * split_ratios[0])
            num_val = max(int(num_trials * split_ratios[1]), 1)  # En az 1 tane val ayır
            for i, trial_path in enumerate(trials):
                if i < num_train:
                    split = "train"
                elif i < num_train + num_val:
                    split = "val"
                else:
                    split = "test"
                data.append([trial_path, person, split])
        else:  # Eğer tekrar sayısı 4 veya daha azsa manuel ayır
            if num_trials == 4:
                splits_assigned = ["train", "train", "val", "test"]
            elif num_trials == 3:
                splits_assigned = ["train", "val", "test"]
            elif num_trials == 2:
                splits_assigned = ["train", "val"]
            else:  # num_trials == 1
                splits_assigned = ["train"]

            for trial_path, split in zip(trials, splits_assigned):
                data.append([trial_path, person, split])

# CSV dosyasına yazma
df = pd.DataFrame(data, columns=["TrialPath", "Label", "Split"])
df.to_csv("dataset.csv", index=False, encoding='utf-8', sep=';')  # UTF-8 ile doğru ayrıştırma

print("CSV dosyası oluşturuldu: dataset.csv")
