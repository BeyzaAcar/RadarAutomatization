from google.colab import drive
import os

def setup_environment():
    """
    Colab ortamını ayarlar:
    - Google Drive bağlantısı yapar
    - Veri setini doğrular
    """
    # Drive'ı bağla
    drive.mount('/content/drive')

    # Dataset dizinini kontrol et
    dataset_dir = "/content/drive/MyDrive/Dataset/LabelledDataset"
    if not os.path.exists(dataset_dir):
        raise FileNotFoundError(f"Dataset klasörü bulunamadı: {dataset_dir}")
    print(f"[INFO] Dataset mevcut: {dataset_dir}")

if __name__ == "__main__":
    setup_environment()
