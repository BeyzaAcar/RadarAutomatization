import os
import numpy as np
import matplotlib.pyplot as plt

def plot_microdoppler(file_path, output_dir):
    """
    Plots the micro-Doppler spectrogram and saves the visualization.
    """
    try:
        # Load spectrogram data
        spectrogram_data = np.load(file_path)
        
        # Plot micro-Doppler spectrogram
        plt.figure(figsize=(10, 6))
        plt.imshow(10 * np.log10(spectrogram_data + 1e-9), aspect='auto', origin='lower')
        plt.colorbar(label="Power (dB)")
        plt.title("Micro-Doppler Spectrogram")
        plt.xlabel("Time Bins")
        plt.ylabel("Frequency Bins")
        
        # Save the plot
        base_name = os.path.basename(file_path).replace('_microdoppler.npy', '_microdoppler.png')
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, base_name)
        plt.savefig(output_path)
        plt.close()
        
        print(f"Micro-Doppler plot saved: {output_path}")
    except Exception as e:
        print(f"Error plotting micro-Doppler spectrogram for {file_path}: {e}")

def process_all_files_in_directory(input_dir, output_dir):
    """
    Generates micro-Doppler plots for all spectrogram files in the input directory.
    """
    spectrogram_files = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if f.endswith('_microdoppler.npy')]
    if not spectrogram_files:
        print(f"No spectrogram files found in directory: {input_dir}")
        return
    
    for file_path in spectrogram_files:
        plot_microdoppler(file_path, output_dir)

if __name__ == "__main__":
    input_dir = "Dataset/ProcessedData/MicroDoppler/"           # Path to micro-Doppler spectrograms
    output_dir = "Dataset/Visualizations/MicroDopplerPlots/"    # Path to save plots
    process_all_files_in_directory(input_dir, output_dir)
