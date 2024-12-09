#Zaman-frekans analizi (STFT) : 
import os
import numpy as np
from scipy.signal import stft
import matplotlib.pyplot as plt

def calculate_spectrogram(file_path, output_dir, fs=1000, nperseg=256):
    """
    Low-pass filtrelenmiş veriye STFT uygular ve spektrogramı kaydeder.
    """
    try:
        # Filtrelenmiş veriyi yükle
        data = np.load(file_path)
        
        # STFT hesapla
        f, t, Zxx = stft(data, fs=fs, nperseg=nperseg)
        magnitude_spectrum = np.abs(Zxx)
        
        # Spektrogramı görselleştir ve kaydet
        base_name = os.path.basename(file_path).replace('_filtered.npy', '_spectrogram.png')
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, base_name)
        plt.pcolormesh(t, f, magnitude_spectrum, shading='gouraud')
        plt.title("Spectrogram")
        plt.ylabel("Frequency (Hz)")
        plt.xlabel("Time (s)")
        plt.colorbar(label="Intensity")
        plt.savefig(output_path)
        plt.close()
        
        print(f"Spektrogram kaydedildi: {output_path}")
    except Exception as e:
        print(f"Hata: {e}")

def process_all_files_in_directory(input_dir, output_dir, fs=1000, nperseg=256):
    """
    Belirtilen klasördeki tüm filtrelenmiş dosyalara STFT uygular.
    """
    npy_files = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if f.endswith('_filtered.npy')]
    if not npy_files:
        print(f"'{input_dir}' klasöründe işlenecek dosya bulunamadı!")
        return
    
    for file_path in npy_files:
        calculate_spectrogram(file_path, output_dir, fs, nperseg)

if __name__ == "__main__":
    input_dir = "Dataset/ProcessedData/Filtered/"
    output_dir = "Dataset/ProcessedData/Spectrograms/"
    process_all_files_in_directory(input_dir, output_dir)
