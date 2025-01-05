import cv2
import os

# AVI dosyalarının bulunduğu klasör
input_dir = "C:/Users/user/Desktop/RADAR_PROJECT/Dataset/CameraData2"  # Buraya AVI dosyalarının bulunduğu klasörün tam yolunu girin
output_dir = "C:/Users/user/Desktop/RADAR_PROJECT/Dataset/ProcessedData/CameraFrames"  # Buraya çıktı klasörünün tam yolunu girin

# Çıktı klasörünü oluştur
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Klasördeki tüm AVI dosyalarını al
avi_files = [f for f in os.listdir(input_dir) if f.endswith(".avi")]

if not avi_files:
    print("Klasörde AVI dosyası bulunamadı.")
else:
    for avi_file in avi_files:
        video_path = os.path.join(input_dir, avi_file)
        video_name = os.path.splitext(avi_file)[0]

        # AVI dosyası için bir klasör oluştur
        video_output_dir = os.path.join(output_dir, video_name)
        if not os.path.exists(video_output_dir):
            os.makedirs(video_output_dir)

        # Frame sayısı ve FPS bilgilerini al
        fps = 25  # Manuel olarak 25 FPS olarak ayarlanıyor
        target_frame_count = 125  # 5 saniye için toplam 125 frame
        frame_index = 0
        extracted_frame_count = 0

        print(f"'{avi_file}' işleniyor: Hedef frame sayısı {target_frame_count}, FPS: {fps}")

        # Zaten hedef frame sayısına ulaşılmış mı kontrol et
        existing_files = len([f for f in os.listdir(video_output_dir) if f.endswith(".png")])
        if existing_files >= target_frame_count:
            print(f"'{avi_file}' için zaten {existing_files} frame mevcut. Atlanıyor.")
            continue

        cap = cv2.VideoCapture(video_path)

        while cap.isOpened() and extracted_frame_count < target_frame_count:
            ret, frame = cap.read()
            if not ret:
                break

            # Frame dosyası zaten var mı kontrol et
            frame_filename = os.path.join(video_output_dir, f"frame_{frame_index}.png")
            if os.path.exists(frame_filename):
                print(f"Frame {frame_index} zaten mevcut. Atlanıyor.")
            else:
                cv2.imwrite(frame_filename, frame)
                extracted_frame_count += 1
                print(f"Frame {frame_index} kaydedildi: {frame_filename}")

            frame_index += 1

        # Kaynakları serbest bırak
        cap.release()
        print(f"'{avi_file}' işleme tamamlandı: Toplam {extracted_frame_count} frame çıkarıldı.")

    print("Tüm AVI dosyaları başarıyla işlendi.")
