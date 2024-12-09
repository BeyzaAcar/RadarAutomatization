import os
import numpy as np
from scipy.signal import butter, filtfilt

def apply_lowpass_filter(data, cutoff, fs, order=5):
    """
    Applies a low-pass Butterworth filter to the input data.
    """
    nyquist = 0.5 * fs
    normal_cutoff = cutoff / nyquist
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return filtfilt(b, a, data)

def process_lowpass(file_path, output_dir, cutoff=50, fs=1000):
    """
    Applies low-pass filtering to the radar data and saves the output.
    """
    try:
        data = np.load(file_path)
        filtered_data = apply_lowpass_filter(data, cutoff, fs)

        # Save filtered data
        base_name = os.path.basename(file_path).replace('_dc_removed.npy', '_filtered.npy')
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, base_name)
        np.save(output_path, filtered_data)
        
        print(f"Low-pass filter applied: {output_path}")
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")

def process_all_files_in_directory(input_dir, output_dir, cutoff=50, fs=1000):
    """
    Applies low-pass filtering to all files in the input directory.
    """
    npy_files = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if f.endswith('_dc_removed.npy')]
    if not npy_files:
        print(f"No files found in directory: {input_dir}")
        return
    
    for file_path in npy_files:
        process_lowpass(file_path, output_dir, cutoff, fs)

if __name__ == "__main__":
    input_dir = "Dataset/ProcessedData/DCRemoved/"  # Path to DC-removed data
    output_dir = "Dataset/ProcessedData/Filtered/"  # Path to save filtered data
    process_all_files_in_directory(input_dir, output_dir)
