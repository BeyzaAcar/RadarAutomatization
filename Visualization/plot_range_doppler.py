import os
import numpy as np
import matplotlib.pyplot as plt

def plot_range_doppler(file_path, output_dir):
    """
    Plots the range-Doppler map from FFT data and saves the visualization.
    """
    try:
        # Load FFT data
        fft_data = np.load(file_path)
        
        # Plot range-Doppler map
        plt.figure(figsize=(10, 6))
        plt.plot(fft_data)
        plt.title("Range-Doppler Map")
        plt.xlabel("Range Bins")
        plt.ylabel("Doppler Magnitude")
        plt.grid()

        # Save the plot
        base_name = os.path.basename(file_path).replace('_fft.npy', '_range_doppler.png')
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, base_name)
        plt.savefig(output_path)
        plt.close()
        
        print(f"Range-Doppler plot saved: {output_path}")
    except Exception as e:
        print(f"Error plotting Range-Doppler map for {file_path}: {e}")

def process_all_files_in_directory(input_dir, output_dir):
    """
    Generates range-Doppler plots for all FFT files in the input directory.
    """
    fft_files = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if f.endswith('_fft.npy')]
    if not fft_files:
        print(f"No FFT files found in directory: {input_dir}")
        return
    
    for file_path in fft_files:
        plot_range_doppler(file_path, output_dir)

if __name__ == "__main__":
    input_dir = "Dataset/ProcessedData/FFT/"               # Path to FFT results
    output_dir = "Dataset/Visualizations/RangeDopplerPlots/"  # Path to save plots
    process_all_files_in_directory(input_dir, output_dir)
