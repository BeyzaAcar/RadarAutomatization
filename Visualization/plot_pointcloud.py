import os
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def plot_pointcloud(file_path, output_dir):
    """
    Visualizes 3D point clouds and saves the plot.
    """
    try:
        # Load point cloud data
        point_cloud = np.load(file_path)
        
        # Extract x, y, z coordinates
        x, y, z = point_cloud[:, 0], point_cloud[:, 1], point_cloud[:, 2]
        
        # Plot the 3D point cloud
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(x, y, z, c='b', marker='o', s=2)
        ax.set_title("3D Point Cloud")
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")
        ax.grid(True)
        
        # Save the plot
        base_name = os.path.basename(file_path).replace('_pointcloud.npy', '_pointcloud.png')
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, base_name)
        plt.savefig(output_path)
        plt.close()
        
        print(f"3D point cloud plot saved: {output_path}")
    except Exception as e:
        print(f"Error plotting 3D point cloud for {file_path}: {e}")

def process_all_files_in_directory(input_dir, output_dir):
    """
    Generates 3D point cloud plots for all files in the input directory.
    """
    pointcloud_files = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if f.endswith('_pointcloud.npy')]
    if not pointcloud_files:
        print(f"No point cloud files found in directory: {input_dir}")
        return
    
    for file_path in pointcloud_files:
        plot_pointcloud(file_path, output_dir)

if __name__ == "__main__":
    input_dir = "Dataset/ProcessedData/PointCloud/"           # Path to point cloud data
    output_dir = "Dataset/Visualizations/PointCloudPlots/"    # Path to save plots
    process_all_files_in_directory(input_dir, output_dir)
