#Mikro-Doppler özellik çıkarımı : 
import os
import numpy as np

def extract_micro_doppler_features(file_path, output_dir):
    """
    Spektrogramdan mikro-Doppler özelliklerini çıkarır ve kaydeder.
    """
    try:
        # Spektrogramı yükle
        spectrogram = np.load(file_path)
        
        # Örnek özellikler: enerji, tepe frekansı, ortalama frekans
        energy = np.sum(spectrogram, axis=1)
        peak_frequency = np.argmax(spectrogram, axis=0)
        mean_frequency = np.mean(peak_frequency)
        
        # Çıktı dosyasını oluştur
        base_name = os.path.basename(file_path).replace('_spectrogram.npy', '_features.npy')
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, base_name)
        
        # Özellikleri kaydet
        np.save(output_path, [energy, peak_frequency, mean_frequency])
        print(f"Özellikler kaydedildi: {output_path}")
    except Exception as e:
        print(f"Hata: {e}")

def process_all_files_in_directory(input_dir, output_dir):
    """
    Belirtilen klasördeki tüm spektrogram dosyalarından özellik çıkarır.
    """
    spectrogram_files = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if f.endswith('_spectrogram.npy')]
    if not spectrogram_files:
        print(f"'{input_dir}' klasöründe işlenecek spektrogram dosyası bulunamadı!")
        return
    
    for file_path in spectrogram_files:
        extract_micro_doppler_features(file_path, output_dir)

if __name__ == "__main__":
    input_dir = "Dataset/ProcessedData/Spectrograms/"
    output_dir = "Dataset/ProcessedData/Features/"
    process_all_files_in_directory(input_dir, output_dir)

    process_all_files_in_directory(input_dir, output_dir)

