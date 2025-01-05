import os
import pandas as pd
import re

def update_experiment_numbers(bin_files_dir, excel_file_path):
    # Excel dosyasını yükle
    try:
        df = pd.read_csv(excel_file_path, delimiter=';')
    except Exception as e:
        print(f"Excel dosyasi okunamadı: {e}")
        return

    # Klasördeki .avi dosyalarını al
    bin_files = [f for f in os.listdir(bin_files_dir) if f.endswith('.avi')]

    if not bin_files:
        print("Klasörde .avi dosyası bulunamadı.")
        return

    for bin_file in bin_files:
        try:
            # Dosya adından kişi ismini çıkar
            match = re.match(r"(.*?)_deney\d+_tekrar\d+_timestamp\d+\.avi", bin_file)
            if not match:
                print(f"{bin_file} için kişi ismi çıkarılamadı.")
                continue

            person_name = match.group(1)

            # Excel'de kişi ismini arayın
            matching_row = df[df['denek_'] == person_name]

            if matching_row.empty:
                print(f"{bin_file} için eşleşen kişi bulunamadı.")
                continue

            # Doğru deney numarasını alın
            experiment_number = matching_row['deney_no'].iloc[0]

            # Yeni dosya adını oluştur
            new_file_name = re.sub(r"_deney\d+", f"_deney{experiment_number}", bin_file)

            # Dosyayı yeniden adlandır
            old_file_path = os.path.join(bin_files_dir, bin_file)
            new_file_path = os.path.join(bin_files_dir, new_file_name)

            os.rename(old_file_path, new_file_path)
            print(f"{bin_file} başarıyla {new_file_name} olarak yeniden adlandırıldı.")

        except Exception as e:
            print(f"{bin_file} için bir hata oluştu: {e}")

if __name__ == "__main__":
    bin_files_dir = r"C:/Users/user/Desktop/RADAR_PROJECT/Dataset/CameraData2"  # Bin dosyalarının olduğu klasör
    excel_file_path = r"C:/Users/user/Desktop/RADAR_PROJECT/Collection/deney_list2.csv"  # Excel dosyasının yolu
    
    update_experiment_numbers(bin_files_dir, excel_file_path)


