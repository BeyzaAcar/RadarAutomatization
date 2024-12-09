import os
import numpy as np

def generate_point_cloud(range_file, angle_file, output_dir):
    """
    Combines range and angle data to generate a 3D point cloud.
    """
    try:
        # Load range and angle data
        range_data = np.load(range_file)
        angle_data = np.load(angle_file)
        
        # Generate point cloud (simple example combining range and angle)
        x = range_data * np.cos(angle_data)
        y = range_data * np.sin(angle_data)
        z = np.zeros_like(range_data)  # Assume a flat plane for simplicity
        
        point_cloud = np.vstack((x, y, z)).T  # Combine into 3D points
        
        # Save point cloud
        base_name = os.path.basename(range_file).replace('_fft.npy', '_pointcloud.npy')
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, base_name)
        np.save(output_path, point_cloud)
        
        print(f"3D point cloud generated: {output_path}")
    except Exception as e:
        print(f"Error generating point cloud for {range_file}: {e}")

def process_all_files_in_directory(range_dir, angle_dir, output_dir):
    """
    Generates 3D point clouds from range and angle data in the input directories.
    """
    range_files = sorted([os.path.join(range_dir, f) for f in os.listdir(range_dir) if f.endswith('_fft.npy')])
    angle_files = sorted([os.path.join(angle_dir, f) for f in os.listdir(angle_dir) if f.endswith('_angles.npy')])
    
    if not range_files or not angle_files:
        print("No range or angle files found for point cloud generation.")
        return
    
    for range_file, angle_file in zip(range_files, angle_files):
        generate_point_cloud(range_file, angle_file, output_dir)

if __name__ == "__main__":
    range_dir = "Dataset/ProcessedData/FFT/"          # Path to FFT results
    angle_dir = "Dataset/ProcessedData/Angles/"       # Path to angle estimation results
    output_dir = "Dataset/ProcessedData/PointCloud/"  # Path to save point clouds
    process_all_files_in_directory(range_dir, angle_dir, output_dir)
