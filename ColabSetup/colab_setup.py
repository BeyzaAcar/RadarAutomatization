import os
import pandas as pd

def setup_colab_environment():
    """
    Colab ortamını ayarlar:
    - Google Drive'ın manuel bağlandığını varsayar
    - Veri setini ve Excel dosyasını Colab çalışma dizinine çeker
    - Kütüphaneleri doğrular
    """
    # Drive'ın bağlı olduğunu kontrol et
    if not os.path.exists("/content/drive"):
        print("[ERROR] Google Drive bağlı değil. Lütfen manuel olarak bağlayın ve yeniden deneyin.")
        return

    # Drive'daki veri seti ve Excel dosyası yolları
    drive_dataset_path = "/content/drive/MyDrive/LabelledDataset"
    drive_excel_path = "/content/drive/MyDrive/dataset_colab.csv"

    # Colab çalışma dizinindeki hedef yollar
    colab_dataset_path = "/content/LabelledDataset"
    colab_excel_path = "/content/dataset_colab.csv"

    # Veri setini Colab'e kopyala
    if not os.path.exists(colab_dataset_path):
        print("[INFO] Veri seti kopyalanıyor...")
        os.system(f"cp -r {drive_dataset_path} {colab_dataset_path}")
        print("[INFO] Veri seti Colab'e kopyalandı.")
    else:
        print("[INFO] Veri seti zaten mevcut.")

    # Excel dosyasını Colab'e kopyala
    if not os.path.exists(colab_excel_path):
        print("[INFO] Excel dosyası kopyalanıyor...")
        os.system(f"cp {drive_excel_path} {colab_excel_path}")
        print("[INFO] Excel dosyası Colab'e kopyalandı.")
    else:
        print("[INFO] Excel dosyası zaten mevcut.")

    # Excel dosyasını kontrol et
    print("[INFO] Excel dosyası doğrulanıyor...")
    df = pd.read_csv(colab_excel_path, sep=';')
    print(df.head())

    print("[INFO] Colab setup tamamlandı. Artık çalışmaya hazırsınız!")

if __name__ == "__main__":
    # Colab ortamını ayarla
    setup_colab_environment()
