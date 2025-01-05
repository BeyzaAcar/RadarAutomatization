import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import spectrogram
from mmwave.dataloader import DCA1000

os.environ['TCL_LIBRARY'] = r"C:\Users\user\AppData\Local\Programs\Python\Python313\tcl\tcl8.6"
os.environ['TK_LIBRARY'] = r"C:\Users\user\AppData\Local\Programs\Python\Python313\tcl\tk8.6"


# Bin dosyalarının olduğu klasör ve görsellerin kaydedileceği klasör
default_bin_folder = r"C:\Users\user\Desktop\RADAR_PROJECT\Dataset\BinData2"
default_output_folder = r"C:\Users\user\Desktop\RADAR_PROJECT\Dataset\ProcessedData\MicroDoppler"

# Radar parametreleri
NUM_TX_ANTENNAS = 3
NUM_RX_ANTENNAS = 4
NUM_CHIRPS_PER_FRAME = 129
NUM_ADC_SAMPLES = 256
NUM_FRAMES = 125
SAMPLE_RATE = 1000  # Örnekleme frekansı (varsayılan)

def process_bin_to_microdoppler(bin_file_path, output_folder):
    """
    Bin dosyasından micro-Doppler spektrogramlarını oluştur ve kaydet.

    Args:
        bin_file_path (str): Bin dosyasının tam yolu.
        output_folder (str): Görsellerin kaydedileceği klasör.
    """
    try:
        # Bin dosyasını yükle
        adc_data = np.fromfile(bin_file_path, dtype=np.uint16)
        adc_data = adc_data.reshape(NUM_FRAMES, -1)

        # ADC verisini düzenle
        adc_data = np.apply_along_axis(
            DCA1000.organize, 1, adc_data,
            num_chirps=NUM_CHIRPS_PER_FRAME,
            num_rx=NUM_RX_ANTENNAS,
            num_samples=NUM_ADC_SAMPLES
        )

        print(f"Veri yüklendi: {bin_file_path} Şekil: {adc_data.shape}")

        # Çıkış klasörünü oluştur
        os.makedirs(output_folder, exist_ok=True)

        # Tüm çerçeveleri işle
        for frame_idx in range(NUM_FRAMES):
            print(f"Frame {frame_idx + 1}/{NUM_FRAMES} işleniyor...")

            # İlgili frame'i al
            frame_data = adc_data[frame_idx]  # Şekil: (chirp, rx, samples)

            # Tüm antenler için STFT uygula
            combined_spectrogram = None
            for rx_idx in range(NUM_RX_ANTENNAS):
                # Her bir anten verisi için STFT
                f, t, Sxx = spectrogram(
                    frame_data[:, rx_idx, :].flatten(),
                    fs=SAMPLE_RATE, nperseg=256
                )

                # Magnitüd spektrumu hesapla (dB)
                Sxx_dB = 10 * np.log10(Sxx + 1e-10)

                # Kombine etmek için antenleri topla
                if combined_spectrogram is None:
                    combined_spectrogram = Sxx_dB
                else:
                    combined_spectrogram += Sxx_dB

            # Görselleştir ve kaydet
            plt.figure(figsize=(12, 6))
            plt.pcolormesh(t, f, combined_spectrogram, shading='gouraud', cmap='jet')
            plt.colorbar(label='Amplitude (dB)')
            plt.title(f"Micro-Doppler Spectrogram - Frame {frame_idx + 1}")
            plt.xlabel("Time (s)")
            plt.ylabel("Frequency (Hz)")

            # Görseli kaydet
            output_path = os.path.join(output_folder, f"MicroDoppler_Frame_{frame_idx + 1}.png")
            plt.savefig(output_path)
            plt.close()

            print(f"Spectrogram kaydedildi: {output_path}")

        print("Tüm frame'ler başarıyla işlendi ve kaydedildi.")

    except Exception as e:
        print(f"Hata oluştu: {e}")

if __name__ == "__main__":
    # Klasörleri ve dosyaları kontrol et
    if not os.path.exists(default_bin_folder):
        print(f"Bin klasörü bulunamadı: {default_bin_folder}")
        exit()

    bin_files = [f for f in os.listdir(default_bin_folder) if f.endswith('.bin')]
    if not bin_files:
        print("Bin dosyası bulunamadı.")
        exit()

    # Her bir bin dosyasını işle
    for bin_file in bin_files:
        bin_path = os.path.join(default_bin_folder, bin_file)
        output_subfolder = os.path.join(default_output_folder, os.path.splitext(bin_file)[0])
        process_bin_to_microdoppler(bin_path, output_subfolder)
