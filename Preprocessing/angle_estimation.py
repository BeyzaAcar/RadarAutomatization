import os
import numpy as np

def estimate_angles(file_path, output_dir):
    """
    Estimates angles using radar data and saves the results.
    """
    try:
        # Load FFT data
        data = np.load(file_path)
        
        # Dummy angle estimation logic (replace with actual AoA method, e.g., MUSIC or FFT-based AoA)
        angles = np.angle(data)  # Placeholder for actual angle computation
        
        # Save estimated angles
        base_name = os.path.basename(file_path).replace('_fft.npy', '_angles.npy')
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, base_name)
        np.save(output_path, angles)
        
        print(f"Angles estimated: {output_path}")
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")

def process_all_files_in_directory(input_dir, output_dir):
    """
    Estimates angles for all FFT radar data files in the input directory.
    """
    npy_files = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if f.endswith('_fft.npy')]
    if not npy_files:
        print(f"No files found in directory: {input_dir}")
        return
    
    for file_path in npy_files:
        estimate_angles(file_path, output_dir)

if __name__ == "__main__":
    input_dir = "Dataset/ProcessedData/FFT/"          # Path to FFT results
    output_dir = "Dataset/ProcessedData/Angles/"      # Path to save angle estimation results
    process_all_files_in_directory(input_dir, output_dir)
