import os
import numpy as np

def remove_dc_offset(file_path, output_dir):
    """
    Removes the DC offset from radar data.
    """
    try:
        # Load raw binary radar data
        data = np.fromfile(file_path, dtype=np.int16)
        
        # Remove DC offset
        processed_data = data - np.mean(data)
        
        # Save the processed data
        base_name = os.path.basename(file_path).replace('.bin', '_dc_removed.npy')
        os.makedirs(output_dir, exist_ok=True)  # Create output directory if it doesn't exist
        output_path = os.path.join(output_dir, base_name)
        np.save(output_path, processed_data)
        
        print(f"DC offset removed: {output_path}")
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")

def process_all_files_in_directory(input_dir, output_dir):
    """
    Processes all .bin files in the input directory to remove DC offset.
    """
    bin_files = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if f.endswith('.bin')]
    if not bin_files:
        print(f"No .bin files found in directory: {input_dir}")
        return
    
    for file_path in bin_files:
        remove_dc_offset(file_path, output_dir)

if __name__ == "__main__":
    input_dir = "Dataset/BinData/"  # Path to raw binary data
    output_dir = "Dataset/ProcessedData/DCRemoved/"  # Path to save processed data
    process_all_files_in_directory(input_dir, output_dir)
