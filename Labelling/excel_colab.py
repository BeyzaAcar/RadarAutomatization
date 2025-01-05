import pandas as pd

def update_paths_for_colab_local(input_csv_path, output_csv_path, colab_base_path):
    """
    Lokal bilgisayardaki Excel dosyasındaki path'leri Colab'e uygun hale getirir.

    Args:
        input_csv_path (str): Mevcut Excel dosyasının yolu (lokal path'ler içerir).
        output_csv_path (str): Yeni oluşturulacak Excel dosyasının yolu.
        colab_base_path (str): Colab'deki LabelledDataset'in temel path'i.
    """
    # Mevcut Excel dosyasını oku
    df = pd.read_csv(input_csv_path, sep=';', header=0)  # İlk satırı başlık olarak al
    print("[INFO] Veri başarıyla okundu.")

    def update_path(path):
        if "LabelledDataset" in path:
            updated_path = colab_base_path + path.split("LabelledDataset", 1)[1].replace("\\", "/")
            return updated_path
        else:
            raise ValueError(f"'LabelledDataset' kısmı bulunamadı: {path}")

    # Path'i güncelle
    df["TrialPath"] = df["TrialPath"].apply(update_path)

    # Güncellenmiş dosyayı kaydet
    df.to_csv(output_csv_path, index=False, sep=';')
    print(f"[INFO] Yeni Excel dosyası oluşturuldu: {output_csv_path}")

if __name__ == "__main__":
    # Mevcut Excel dosyasının yolu (lokal path'ler içerir)
    input_csv = r"C:/Users/user/Desktop/RADAR_PROJECT/Labelling/dataset.csv"

    # Yeni oluşturulacak Excel dosyasının yolu
    output_csv = r"C:/Users/user/Desktop/RADAR_PROJECT/Labelling/dataset_colab.csv"

    # Colab'deki LabelledDataset'in temel path'i
    colab_base_path = "/content/LabelledDataset"

    # Path'leri güncelle
    update_paths_for_colab_local(input_csv, output_csv, colab_base_path)
