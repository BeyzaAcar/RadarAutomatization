import os
import numpy as np

def calculate_fft(file_path, output_dir):
    """
    Applies FFT to the filtered radar data and saves the output.
    """
    try:
        # Load filtered radar data
        data = np.load(file_path)
        
        # Apply FFT
        fft_data = np.fft.fft(data)
        fft_magnitude = np.abs(fft_data[:len(fft_data)//2])  # Use only positive frequencies
        
        # Save FFT results
        base_name = os.path.basename(file_path).replace('_filtered.npy', '_fft.npy')
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, base_name)
        np.save(output_path, fft_magnitude)
        
        print(f"FFT applied: {output_path}")
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")

def process_all_files_in_directory(input_dir, output_dir):
    """
    Applies FFT to all filtered radar data files in the input directory.
    """
    npy_files = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if f.endswith('_filtered.npy')]
    if not npy_files:
        print(f"No files found in directory: {input_dir}")
        return
    
    for file_path in npy_files:
        calculate_fft(file_path, output_dir)

if __name__ == "__main__":
    input_dir = "Dataset/ProcessedData/Filtered/"  # Path to filtered data
    output_dir = "Dataset/ProcessedData/FFT/"      # Path to save FFT results
    process_all_files_in_directory(input_dir, output_dir)
