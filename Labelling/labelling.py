import os
import shutil

def organize_labelled_dataset(bin_data_dir, camera_data_dir, micro_doppler_dir, range_doppler_dir, output_dir):
    """
    Organizes labelled dataset into a structured format.

    Args:
        bin_data_dir (str): Path to the BinData directory.
        camera_data_dir (str): Path to the CameraData directory.
        micro_doppler_dir (str): Path to the MicroDoppler directory.
        range_doppler_dir (str): Path to the RangeDoppler directory.
        output_dir (str): Path to save the organized dataset.
    """
    os.makedirs(output_dir, exist_ok=True)

    def extract_person_name(file_name):
        """Extracts the person's name from the file name."""
        return file_name.split('_deney')[0]

    def copy_files(src, dest, file_type):
        """Copies files from source to destination based on the file type."""
        if not os.path.exists(src):
            print(f"[WARNING] Source directory does not exist: {src}")
            return

        for file_name in os.listdir(src):
            if file_name.endswith(file_type):
                person_name = extract_person_name(file_name)
                person_dir = os.path.join(dest, person_name)
                os.makedirs(person_dir, exist_ok=True)

                if file_type == '.bin':
                    target_subdir = os.path.join(person_dir, 'BinData')
                elif file_type == '.avi':
                    target_subdir = os.path.join(person_dir, 'CameraData')
                else:
                    continue

                os.makedirs(target_subdir, exist_ok=True)
                shutil.copy(os.path.join(src, file_name), os.path.join(target_subdir, file_name))

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
            else:
                continue

            os.makedirs(target_subdir, exist_ok=True)
            shutil.copytree(os.path.join(src, folder_name), os.path.join(target_subdir, folder_name))

    # Copy files and folders to the organized structure
    copy_files(bin_data_dir, output_dir, '.bin')
    copy_files(camera_data_dir, output_dir, '.avi')
    copy_folders(micro_doppler_dir, output_dir, 'MicroDoppler')
    copy_folders(range_doppler_dir, output_dir, 'RangeDoppler')

    print(f"Labelled dataset organized successfully in: {output_dir}")

if __name__ == "__main__":
    bin_data_directory = r"C:\Users\user\Desktop\RADAR_PROJECT\Dataset\DenemeBin"
    camera_data_directory = r"C:\Users\user\Desktop\RADAR_PROJECT\Dataset\DenemeCamera"
    micro_doppler_directory = r"C:\Users\user\Desktop\RADAR_PROJECT\Dataset\DenemeMicroDoppler"
    range_doppler_directory = r"C:\Users\user\Desktop\RADAR_PROJECT\Dataset\DenemeRangeDoppler"
    output_directory = r"C:\Users\user\Desktop\RADAR_PROJECT\Dataset\LabelledDataset"

    organize_labelled_dataset(
        bin_data_dir=bin_data_directory,
        camera_data_dir=camera_data_directory,
        micro_doppler_dir=micro_doppler_directory,
        range_doppler_dir=range_doppler_directory,
        output_dir=output_directory
    )
