import os
import numpy as np

def remove_dc_offset(file_path, output_dir):
    """
    Ham radar verisini okuyup DC offset'i kaldırır ve kaydeder.
    """
    try:
        # Ham veriyi oku
        data = np.fromfile(file_path, dtype=np.int16)
        # DC Offset kaldırma
        processed_data = data - np.mean(data)
        
        # Çıktı dosyasını oluştur
        base_name = os.path.basename(file_path).replace('.bin', '_dc_removed.npy')
        os.makedirs(output_dir, exist_ok=True)  # Çıktı klasörü yoksa oluştur
        output_path = os.path.join(output_dir, base_name)
        
        # İşlenmiş veriyi kaydet
        np.save(output_path, processed_data)
        print(f"DC offset kaldırılmış veri kaydedildi: {output_path}")
    except Exception as e:
        print(f"Hata: {e}")

def process_all_files_in_directory(input_dir, output_dir):
    """
    Belirtilen klasördeki tüm .bin dosyalarına DC offset kaldırma işlemi uygular.
    """
    bin_files = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if f.endswith('.bin')]
    if not bin_files:
        print(f"'{input_dir}' klasöründe işlenecek .bin dosyası bulunamadı!")
        return
    
    for file_path in bin_files:
        remove_dc_offset(file_path, output_dir)

if __name__ == "__main__":
    input_dir = "Dataset/BinData/"
    output_dir = "Dataset/ProcessedData/DCRemoved/"
    process_all_files_in_directory(input_dir, output_dir)
