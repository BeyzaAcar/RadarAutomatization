import os
import numpy as np
from scipy.signal import butter, lfilter

def butter_lowpass_filter(data, cutoff, fs, order=5):
    nyquist = 0.5 * fs
    normal_cutoff = cutoff / nyquist
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    y = lfilter(b, a, data)
    return y

def apply_lowpass_filter(file_path, output_dir, cutoff=100, fs=1000):
    """
    DC offset kaldırılmış veriye low-pass filtre uygular ve sonucu kaydeder.
    """
    try:
        # DC offset kaldırılmış veriyi yükle
        data = np.load(file_path)
        # Low-pass filtre uygula
        filtered_data = butter_lowpass_filter(data, cutoff=cutoff, fs=fs, order=4)
        
        # Çıktı dosyasını oluştur
        base_name = os.path.basename(file_path).replace('_dc_removed.npy', '_filtered.npy')
        os.makedirs(output_dir, exist_ok=True)  # Çıktı klasörü yoksa oluştur
        output_path = os.path.join(output_dir, base_name)
        
        # Filtrelenmiş veriyi kaydet
        np.save(output_path, filtered_data)
        print(f"Filtrelenmiş veri kaydedildi: {output_path}")
    except Exception as e:
        print(f"Hata: {e}")

def process_all_files_in_directory(input_dir, output_dir, cutoff=100, fs=1000):
    """
    Belirtilen klasördeki tüm DC offset kaldırılmış dosyalara low-pass filtre uygular.
    """
    npy_files = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if f.endswith('_dc_removed.npy')]
    if not npy_files:
        print(f"'{input_dir}' klasöründe işlenecek dosya bulunamadı!")
        return
    
    for file_path in npy_files:
        apply_lowpass_filter(file_path, output_dir, cutoff, fs)

if __name__ == "__main__":
    input_dir = "Dataset/ProcessedData/DCRemoved/"
    output_dir = "Dataset/ProcessedData/Filtered/"
    process_all_files_in_directory(input_dir, output_dir)
