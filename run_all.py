import os
import subprocess

# Function to run a script
def run_script(script_path, description):
    try:
        print(f"Running: {description}")
        subprocess.run(["python", script_path], check=True)
        print(f"Completed: {description}\n")
    except subprocess.CalledProcessError as e:
        print(f"Error in {description}: {e}\n")

def main():
    print("Starting the Radar Data Processing Pipeline...\n")

    # Define script paths
    preprocessing_scripts = [
        ("Preprocessing/dc_offset_removal.py", "DC Offset Removal"),
        ("Preprocessing/lowpass_filter.py", "Low-Pass Filtering"),
        ("Preprocessing/fft_processing.py", "FFT Processing"),
        ("Preprocessing/microdoppler_stft.py", "Micro-Doppler Spectrogram Generation"),
        ("Preprocessing/angle_estimation.py", "Angle Estimation"),
        ("Preprocessing/radar_to_pointcloud.py", "3D Point Cloud Generation")
    ]

    visualization_scripts = [
        ("Visualization/plot_range_doppler.py", "Range-Doppler Map Visualization"),
        ("Visualization/plot_microdoppler.py", "Micro-Doppler Spectrogram Visualization"),
        ("Visualization/plot_pointcloud.py", "3D Point Cloud Visualization")
    ]

    # Run preprocessing scripts
    print("=== Preprocessing ===\n")
    for script_path, description in preprocessing_scripts:
        run_script(script_path, description)

    # Run visualization scripts
    print("=== Visualization ===\n")
    for script_path, description in visualization_scripts:
        run_script(script_path, description)

    print("Pipeline completed successfully!")

if __name__ == "__main__":
    main()
