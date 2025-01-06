import os
import shutil

def organize_labelled_dataset(bin_data_dir, camera_data_dir, micro_doppler_dir, range_doppler_dir, camera_frames_dir, output_dir):
    """
    Organizes labelled dataset into a structured format.

    Args:
        bin_data_dir (str): Path to the BinData directory.
        camera_data_dir (str): Path to the CameraData directory.
        micro_doppler_dir (str): Path to the MicroDoppler directory.
        range_doppler_dir (str): Path to the RangeDoppler directory.
        camera_frames_dir (str): Path to the CameraFrames directory.
        output_dir (str): Path to save the organized dataset.
    """
    os.makedirs(output_dir, exist_ok=True)

    def extract_person_name(file_name):
        """Extracts the person's name from the file name."""
        return file_name.split('_deney')[0]

    # def copy_files(src, dest, file_type):
    #     """Copies files from source to destination based on the file type."""
    #     if not os.path.exists(src):
    #         print(f"[WARNING] Source directory does not exist: {src}")
    #         return

    #     for file_name in os.listdir(src):
    #         if file_name.endswith(file_type):
    #             person_name = extract_person_name(file_name)
    #             person_dir = os.path.join(dest, person_name)
    #             os.makedirs(person_dir, exist_ok=True)

    #             if file_type == '.bin':
    #                 target_subdir = os.path.join(person_dir, 'BinData')
    #             elif file_type == '.avi':
    #                 target_subdir = os.path.join(person_dir, 'CameraData')
    #             else:
    #                 continue

    #             os.makedirs(target_subdir, exist_ok=True)
    #             shutil.copy(os.path.join(src, file_name), os.path.join(target_subdir, file_name))

    def copy_folders(src, dest, folder_type):
        """Copies folders from source to destination."""
        if not os.path.exists(src):
            print(f"[WARNING] Source directory does not exist: {src}")
            return

        for folder_name in os.listdir(src):
            person_name = extract_person_name(folder_name)
            person_dir = os.path.join(dest, person_name)
            os.makedirs(person_dir, exist_ok=True)

            if folder_type == 'MicroDoppler':
                target_subdir = os.path.join(person_dir, 'MicroDoppler')
            elif folder_type == 'RangeDoppler':
                target_subdir = os.path.join(person_dir, 'RangeDoppler')
            elif folder_type == 'CameraFrames':
                target_subdir = os.path.join(person_dir, 'CameraFrames')
            else:
                continue

            os.makedirs(target_subdir, exist_ok=True)
            shutil.copytree(os.path.join(src, folder_name), os.path.join(target_subdir, folder_name))

    # Copy files and folders to the organized structure
    # copy_files(bin_data_dir, output_dir, '.bin')
    # copy_files(camera_data_dir, output_dir, '.avi')
    # copy_folders(micro_doppler_dir, output_dir, 'MicroDoppler')
    copy_folders(range_doppler_dir, output_dir, 'RangeDoppler')
    copy_folders(camera_frames_dir, output_dir, 'CameraFrames')

    print(f"Labelled dataset organized successfully in: {output_dir}")

if __name__ == "__main__":
    bin_data_directory = "/content/drive/MyDrive/Dataset/BinData2"
    camera_data_directory = "/content/drive/MyDrive/LabelledData/CameraData2"
    micro_doppler_directory = "/content/drive/MyDrive/MicroDoppler"
    range_doppler_directory = "/content/drive/MyDrive/LabelledData/RangeDoppler"
    camera_frames_directory = "/content/drive/MyDrive/LabelledData/CameraFrames"
    output_directory = "/content/drive/MyDrive/Labelled_Dataset"

    organize_labelled_dataset(
        bin_data_dir=bin_data_directory,
        camera_data_dir=camera_data_directory,
        micro_doppler_dir=micro_doppler_directory,
        range_doppler_dir=range_doppler_directory,
        camera_frames_dir=camera_frames_directory,
        output_dir=output_directory
    )
