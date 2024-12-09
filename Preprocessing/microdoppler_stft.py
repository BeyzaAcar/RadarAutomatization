import os
import numpy as np
from scipy.signal import spectrogram

def generate_microdoppler(file_path, output_dir, fs=1000, nperseg=256):
    """
    Generates a spectrogram (micro-Doppler signature) from radar data.
    """
    try:
        # Load FFT data
        data = np.load(file_path)
        
        # Generate spectrogram
        f, t, Sxx = spectrogram(data, fs=fs, nperseg=nperseg)
        
        # Save spectrogram
        base_name = os.path.basename(file_path).replace('_fft.npy', '_microdoppler.npy')
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, base_name)
        np.save(output_path, Sxx)
        
        print(f"Micro-Doppler signature generated: {output_path}")
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")

def process_all_files_in_directory(input_dir, output_dir, fs=1000, nperseg=256):
    """
    Applies micro-Doppler signature generation to all FFT radar data files.
    """
    npy_files = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if f.endswith('_fft.npy')]
    if not npy_files:
        print(f"No files found in directory: {input_dir}")
        return
    
    for file_path in npy_files:
        generate_microdoppler(file_path, output_dir, fs, nperseg)

if __name__ == "__main__":
    input_dir = "Dataset/ProcessedData/FFT/"           # Path to FFT results
    output_dir = "Dataset/ProcessedData/MicroDoppler/" # Path to save spectrograms
    process_all_files_in_directory(input_dir, output_dir)
