import os
import numpy as np

def calculate_fft(file_path, output_dir):
    """
    Filtrelenmiş veriye FFT uygular ve sonucu kaydeder.
    """
    try:
        # Filtrelenmiş veriyi yükle
        data = np.load(file_path)
        # FFT uygula
        fft_data = np.fft.fft(data)
        fft_magnitude = np.abs(fft_data[:len(fft_data)//2])  # Yalnızca pozitif frekanslar
        
        # Çıktı dosyasını oluştur
        base_name = os.path.basename(file_path).replace('_filtered.npy', '_fft.npy')
        os.makedirs(output_dir, exist_ok=True)  # Çıktı klasörü yoksa oluştur
        output_path = os.path.join(output_dir, base_name)
        
        # FFT verisini kaydet
        np.save(output_path, fft_magnitude)
        print(f"FFT sonucu kaydedildi: {output_path}")
    except Exception as e:
        print(f"Hata: {e}")

def process_all_files_in_directory(input_dir, output_dir):
    """
    Belirtilen klasördeki tüm filtrelenmiş dosyalara FFT uygular.
    """
    npy_files = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if f.endswith('_filtered.npy')]
    if not npy_files:
        print(f"'{input_dir}' klasöründe işlenecek dosya bulunamadı!")
        return
    
    for file_path in npy_files:
        calculate_fft(file_path, output_dir)

if __name__ == "__main__":
    input_dir = "Dataset/ProcessedData/Filtered/"
    output_dir = "Dataset/ProcessedData/FFT/"
    process_all_files_in_directory(input_dir, output_dir)
