import matplotlib
matplotlib.use('Agg')  # <-- GUI yerine 'Agg' backend kullanıyoruz

import os
import numpy as np
import matplotlib.pyplot as plt
from mmwave.dataloader import DCA1000
import mmwave.dsp as dsp

bin_dosyaları_klasörü_yolu = r"C:\Users\user\Desktop\RADAR_PROJECT\Dataset\BinData2"
gorseller_klasoru_yolu = r"C:\Users\user\Desktop\RADAR_PROJECT\Dataset\ProcessedData\RangeDoppler"

def process_bin_to_images(file_path, output_folder):
    """
    Eğer 'output_folder' zaten varsa ve yeniden oluşturmak istemiyorsanız
    fonksiyonu hemen return ile sonlandırıyoruz.
    """
    if os.path.exists(output_folder):
        print(f"[INFO] {output_folder} zaten mevcut. İşleme alınmadı.")
        return  # Klasör zaten varsa, işlem yapmıyoruz.

    # Çıkmıyorsak, yani klasör yoksa burada oluşturacağız:
    os.makedirs(output_folder, exist_ok=True)

    num_tx_antennas = 3
    numChirpsPerFrame = 129
    numFrames = 125
    numRxAntennas = 4
    numADCSamples = 256

    adc_data = np.fromfile(file_path, dtype=np.uint16)
    adc_data = adc_data.reshape(numFrames, -1)
    adc_data = np.apply_along_axis(
        DCA1000.organize, 1, adc_data,
        num_chirps=numChirpsPerFrame,
        num_rx=numRxAntennas,
        num_samples=numADCSamples
    )

    print(f"Data Loaded from {file_path} with shape {adc_data.shape}")

    for i in range(numFrames):
        frame = adc_data[i]
        range_fft_data = np.fft.fft(frame, axis=-1)

        # -----------------------------------------------------
        # CHIRP sayısını 3'e tam bölünecek şekilde "PAD" (sıfır ekle)
        # 128 chirp'i 129'a (veya 132'ye) çıkararak 3'e bölünebilecek hale getiriyoruz.
        # -----------------------------------------------------
        valid_chirp_count = (
            (range_fft_data.shape[0] + (num_tx_antennas - 1)) 
            // num_tx_antennas
        ) * num_tx_antennas
        pad_size = valid_chirp_count - range_fft_data.shape[0]
        
        if pad_size > 0:
            print(f"[WARNING] Padding {pad_size} chirps with zeros "
                  f"to make it divisible by num_tx_antennas={num_tx_antennas}.")
            pad_shape = (pad_size,) + range_fft_data.shape[1:]  # (eklenecek_satır, Rx, numADCSamples)
            pad_zeros = np.zeros(pad_shape, dtype=range_fft_data.dtype)
            range_fft_data = np.concatenate((range_fft_data, pad_zeros), axis=0)

        # Artık range_fft_data.shape[0] % 3 == 0
        fft2d_in = dsp.separate_tx(range_fft_data, num_tx_antennas, vx_axis=1, axis=0)
        fft2d_in = np.transpose(fft2d_in, axes=(2, 1, 0))
        fft2d_out = np.fft.fft(fft2d_in)

        fft2d_log_abs = 40 * np.log10(np.abs(fft2d_out) + 1e-10)
        det_matrix = np.sum(fft2d_log_abs, axis=1)
        det_matrix_vis = np.fft.fftshift(det_matrix, axes=1)

        plt.figure(figsize=(12, 6))
        plt.imshow(det_matrix_vis / det_matrix_vis.max(), aspect='auto', cmap='jet')
        plt.title(f"Range-Doppler plot {i} - {os.path.basename(file_path)}")
        plt.colorbar(label='Amplitude (dBFS)')
        plt.xlabel('Range-fft')
        plt.ylabel('Doppler-fft')

        plt.savefig(os.path.join(output_folder, f'RangeDoppler_{i}.png'))
        plt.close()

bin_files_found = False
for file_name in os.listdir(bin_dosyaları_klasörü_yolu):
    if file_name.endswith('.bin'):
        bin_files_found = True
        file_path = os.path.join(bin_dosyaları_klasörü_yolu, file_name)
        klasor_yolu_isimli = os.path.join(
            gorseller_klasoru_yolu, 
            os.path.splitext(file_name)[0]
        )
        process_bin_to_images(file_path, klasor_yolu_isimli)

if not bin_files_found:
    print("Klasörde '.bin' uzantılı dosya bulunamadı.")

print("Görseller oluşturma işlemi tamamlandı.")
