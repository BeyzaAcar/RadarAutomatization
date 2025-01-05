import csv
import os

def update_csv(args, tekrar_index):
    csv_file_path = "deney_list2.csv"
    header = [
        "deney_no", "denek_", "duration_", "kayit_fps_", "tekrar_",
        "tekrar_beklemesi_", "delay_", "cinsiyet_", "mekan_", 
        "bilgisayar_", "kisi_sayisi_", "elbise_",
        "num_chirps_", "num_rx_", "num_tx_", "num_frames_", "adc_sample_"
    ]
    
    # Eğer CSV yoksa veya başlıklar eksikse başlığı yaz
    if not os.path.exists(csv_file_path) or os.stat(csv_file_path).st_size == 0:
        with open(csv_file_path, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(header)
    
    # Dosya mevcutsa, son satırdaki deney_no ve denek_ değerini al
    deney_no = 1
    last_denek = None
    if os.path.exists(csv_file_path) and os.stat(csv_file_path).st_size > 0:
        with open(csv_file_path, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file, delimiter=';')
            rows = list(reader)
            if len(rows) > 1:  # Eğer en az bir satır veri varsa
                last_row = rows[-1]
                deney_no = int(last_row[0])  # İlk sütun (deney_no) okunur
                last_denek = last_row[1]    # İkinci sütun (denek_) okunur
    
    # Yeni kişi için deney_no artırılır
    if args.denek_ != last_denek:
        deney_no += 1
    
    # Yeni kayıt için verileri hazırla
    row = [
        deney_no, args.denek_, args.duration_, args.kayit_fps_,
        tekrar_index, args.tekrar_beklemesi_, args.delay_,
        args.cinsiyet_, args.mekan_, args.bilgisayar_, args.kisi_sayisi_, args.elbise_,
        args.num_chirps_, args.num_rx_, args.num_tx_, args.num_frames_, args.adc_sample_
    ]
    
    # Yeni satırı dosyaya ekle
    with open(csv_file_path, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(row)
