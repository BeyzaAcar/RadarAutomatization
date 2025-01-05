import os
import time
import threading
import winsound
import pyautogui
import cv2
import argparse
import shutil

from csv_handler import update_csv # csv_handler.py dosyasindan update_csv fonksiyonunu import et (deney_list.csv dosyasini güncellemek için)

# Ses Çalma
def play_start_sound():
    winsound.Beep(2500, 500)  # Başlangiç sesi

def play_end_sound():
    winsound.Beep(500, 500)  # Bitiş sesi

def play_ready_sound():
    winsound.Beep(1500, 500)  # Hazır sesi


# Kamera Kaydi
def record_camera(duration, output_path, fps, barrier):
    barrier.wait()
    cap = cv2.VideoCapture(0)  # Bilgisayar kamerasini aç
    fourcc = cv2.VideoWriter_fourcc(*'XVID')  # Video formati
    out = cv2.VideoWriter(output_path, fourcc, fps, (640, 480))  # Video dosyasi
    
    start_time = time.time()
    while int(time.time() - start_time) < duration:
        ret, frame = cap.read()
        if ret:
            out.write(frame)  # Frame kaydet
        else:
            break
        
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    # Radar Verisi Toplama


def collect_radar_data(bin_output_path, dcax, dcay, trgx, trgy, delay, barrier):
    # PyAutoGUI ile radar tuşlarina tiklama
    pyautogui.click(x=dcax, y=dcay)
    time.sleep(delay)  # DCA ve Trigger arasinda bekleme süresi
    barrier.wait()
    pyautogui.click(x=trgx, y=trgy)

    #play start sound
    play_start_sound()

    # Bin dosyasini bekle ve kopyala
    radar_bin_path = r"C:\ti\mmwave_studio_02_01_01_00\mmWaveStudio\PostProc\adc_data_Raw_0.bin"
    wait_time = 0
    max_wait = 5  # Maksimum bekleme süresi (saniye)
    while not os.path.exists(radar_bin_path):
        if wait_time >= max_wait:
            print("Radar bin dosyasi bulunamadi! Süre doldu.")
            return
        print("Bin dosyasi bekleniyor...")
        time.sleep(1)
        wait_time += 1


    time.sleep(10) # Dosyanin yazilmasi için bekleme süresi

   # Dosyayi tasi
    try:
        shutil.move(radar_bin_path, bin_output_path)  # Dosyayi hedef konuma tasi
        print(f"Radar bin dosyasi başariyla taşindi: {bin_output_path}")
    except Exception as e:
        print(f"Dosya taşima sirasinda hata oluştu: {e}")

def prepare_camera():
    cap = cv2.VideoCapture(0)  # Kamera başlatılır
    if not cap.isOpened():
        print("Kamera açılamadı!")
        return None
    print("Kamera hazır.")  # Kamera hazır mesajı
    return cap

def record_camera_with_sync(duration, output_path, fps, barrier, cap):
    barrier.wait()  # Senkronizasyon noktası
    fourcc = cv2.VideoWriter_fourcc(*'XVID')  # Video formatı
    out = cv2.VideoWriter(output_path, fourcc, fps, (640, 480))  # Video dosyası

    start_time = time.time()
    while int(time.time() - start_time) < duration:
        ret, frame = cap.read()  # Kameradan kare al
        if ret:
            out.write(frame)  # Kareyi kaydet
        else:
            print("Kare alınamadı!")
            break

    out.release()  # Video kaydını kapat
    print("Kamera kaydı tamamlandı.")


# Ana Program
def main():
    barrier = threading.Barrier(2)

    # play ready sound
    play_ready_sound()

    # Kamerayı önceden hazırla
    cap = prepare_camera()
    if not cap:
        print("Kamera başlatılamadı, program sonlanıyor.")
        return

    # Argümanlari Tanimla
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--denek_', default='simal_sayar', help='Denek adi veya ID\'si (varsayilan: doga_def)')
    parser.add_argument('--kisi_sayisi_', type=int, default=1, help='Oda içinde kaç kişi olduğu (varsayilan: 1)')
    parser.add_argument('--elbise_', default='normal', help='Denek elbise bilgisi (varsayilan: bilgi_yok)')
    parser.add_argument('--cinsiyet_', default='kadin', help='Denek cinsiyeti ()')

    # add adc_sample, num_chirps, num_rx, num_tx, num_frames
    parser.add_argument('--adc_sample_', type=int, default=256, help='ADC örnekleme sayisi (varsayilan: 256)')
    parser.add_argument('--num_chirps_', type=int, default=129, help='Bir frame\'deki chirp sayisi (varsayilan: 128)')
    parser.add_argument('--num_rx_', type=int, default=4, help='alici anten sayisi (varsayilan: 4)')
    parser.add_argument('--num_tx_', type=int, default=3, help='Verici anten sayisi (varsayilan: 3)')
    parser.add_argument('--num_frames_', type=int, default=125, help='Bir dosyadaki frame sayisi (varsayilan: 128)')

    parser.add_argument('--mekan_', default='yurt_yemekhane', help='Deneyin yapildiği mekan bilgisi (varsayilan: ev)')
    parser.add_argument('--kayit_fps_', type=int, default=25, help='Kameranin kayittaki FPS değeri (varsayilan: 30)')
    parser.add_argument('--duration_', type=float, default=5, help='Kamera kaydinin süresi (saniye) (varsayilan: 10)')
    parser.add_argument('--tekrar_', type=int, default=4, help='Kaydin kaç defa tekrarlanacaği (varsayilan: 1)')
    
    parser.add_argument('--deney_no_', type=int, default=1, help='Deney numarasi (varsayilan: 1)')
    parser.add_argument('--tekrar_beklemesi_', type=float, default=1, help='Tekrarlar arasindaki bekleme süresi (saniye) (varsayilan: 1)')
    parser.add_argument('--dcax_', type=int, default=886, help='DCA düğmesinin X koordinati (varsayilan: 886)')
    parser.add_argument('--dcay_', type=int, default=452, help='DCA düğmesinin Y koordinati (varsayilan: 452)')
    parser.add_argument('--trgx_', type=int, default=951, help='Tetikleyici düğmesinin X koordinati (varsayilan: 951)')
    parser.add_argument('--trgy_', type=int, default=445, help='Tetikleyici düğmesinin Y koordinati (varsayilan: 445)')
    parser.add_argument('--bilgisayar_', default='asus', help='İşletim sistemi bilgisi (varsayilan: windows)')
    parser.add_argument('--delay_', type=int, default=1, help='DCA ve Trigger arasindaki bekleme süresi (saniye) (varsayilan: 2)')



    

    # timestamp 
    timestamp = int(time.time())

    # Argümanlari Parse Et
    args = parser.parse_args()

    # Sleep delay for 
    time.sleep(2)

    for tekrar_index in range(1, args.tekrar_ + 1):
        print(f"Tekrar {tekrar_index}/{args.tekrar_}")
        
        # Dinamik dosya yolu keyfi yaptşk burda (her tekrar için farkli dosya yolu) (timestamp eklicem)
        bin_output_path = os.path.expanduser(f"C:/Users/user/Desktop/RADAR_PROJECT/Dataset/BinData2/{args.denek_}_deney{args.deney_no_}_tekrar{tekrar_index}_timestamp{timestamp}.bin")
        camera_output_path = os.path.expanduser(f"C:/Users/user/Desktop/RADAR_PROJECT/Dataset/CameraData2/{args.denek_}_deney{args.deney_no_}_tekrar{tekrar_index}_timestamp{timestamp}.avi")

        # Klasörlerin varliğini kontrol et ve gerekirse oluştur
        os.makedirs(os.path.dirname(bin_output_path), exist_ok=True)
        os.makedirs(os.path.dirname(camera_output_path), exist_ok=True)

        
        # Radar ve Kamera için iş parçaciklarini başlat
        radar_thread = threading.Thread(
            target=collect_radar_data,
            args=(bin_output_path, args.dcax_, args.dcay_, args.trgx_, args.trgy_, args.delay_, barrier)
        )
        camera_thread = threading.Thread(
            target=record_camera_with_sync,
            args=(args.duration_, camera_output_path, args.kayit_fps_, barrier, cap)
        )

        # Ayni anda başlat
        radar_thread.start()
        camera_thread.start()
        
        # İşlemlerin bitmesini bekle
        radar_thread.join()
        camera_thread.join()

        # play ready sound if tekrar_index < args.tekrar_
        if tekrar_index < args.tekrar_:
            play_ready_sound()

        # CSV dosyasini güncelle
        update_csv(args, tekrar_index) # tekrar_index + 1 çünkü 0'dan başlamiyoruz (tekrar1, tekrar2, ...)
        
        # Bekleme süresi
        if tekrar_index < args.tekrar_:
            print("Bir sonraki tekrar için bekleniyor...")
            time.sleep(args.tekrar_beklemesi_)


    # Bitiş Sesi
    play_end_sound()
    print("Radar ve kamera verisi toplama tamamlandi!")

if __name__ == "__main__":
    main()




# TODO 1: deney_list.csv dosyasi oluşturulacak ve deneyler buraya kaydedilecek (denek_adi, deney_no, zaman_damgasi, radar_path, kamera_path falan olabilir)
# TODO 2: deney_list.csv dosyasi okunacak ve deneyler sirayla çaliştirilacak ( her birine ayri id verilecek )
# TODO 3: deneylerin başlangiç ve bitiş zamanlari, süreleri, başarili olup olmadiği, hata durumlari, vb. kaydedilecek (log dosyasi oluşturulacak)
# TODO 4: deneylerin zaman damgasi (timestamp) otomatik olarak atanacak ve linux zaman damgasi formatina çevrilecek ki kisa olsun
# TODO 5: ÇOK ÖNEMLİ: deneylerin parametrelerini diğer kodla karşilaştir ki tam ayni olsun, örneğin iki tekrar yapiliyorsa, isimlendirmeleri farkli olmali. 
# TODO 6: Bütün ama bütünnn parametreleri netleştir. DİĞER KODLA KARŞILAŞTIRARAK.
# TODO 7: line 112 deki timestampi ekleyeceğim. İki threadin ayni anda başlamasi için


# UNIX Time display url : https://time.is/Unix_time#google_vignette  (display unix time from screen)



# BILINMESI GEREKENLER :
    # 1. time.time() fonksiyonu unix zaman damgasini verir (saniye cinsinden)
    # 2. timestamp kod çalişmaya başladiğinda alinir ve her bir tekrar için ayni olur (tekrar numarasina göre farki bulunabilir dosya adinda tekrar1, tekrar2 gibi yazacak)
    # 3. cinsiyet 0: erkek, 1: kadin, 2: bilgi yok

# KODU ÇALIŞTIRMAK İÇİN :
    # 1. cmd'yi aç
    # 2. python auto_radar.py --denek_ doga_def --deney_no_ 1 --duration_ 10 --kayit_fps_ 30 --tekrar_ 2 --tekrar_beklemesi_ 1 --mekan_ ev --dcax_ 886 --dcay_ 452 --trgx_ 951 --trgy_ 445 --elbise_ bilgi_yok --bilgisayar_ windows
    # 3. kodu çaliştir
    # 4. işlem bitince ses çalacak ve ekrana "Radar ve kamera verisi toplama tamamlandi!" yazacak (kodun çaliştiği ekrana bak)