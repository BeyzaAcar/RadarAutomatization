import csv
import os

def update_csv(args, tekrar_index):
    csv_file_path = "deney_list.csv"
    header = [
        "deney_no", "denek_", "duration_", "kayit_fps_", "tekrar_",
        "tekrar_beklemesi_", "delay_", "cinsiyet_", "mekan_", 
        "dcax_", "dcay_", "trgx_", "trgy_"
    ]
    
    # Eğer CSV yoksa veya başlıklar eksikse başlığı yaz
    if not os.path.exists(csv_file_path) or os.stat(csv_file_path).st_size == 0:
        with open(csv_file_path, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file, delimiter=';')  # Noktalı virgül ayırıcıyı burada da kullan
            writer.writerow(header)
    
    # Dosya mevcutsa, son satırdaki deney_no değerini al ve bir artır
    deney_no = 1
    if os.path.exists(csv_file_path) and os.stat(csv_file_path).st_size > 0:
        with open(csv_file_path, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file, delimiter=';')  # Okuma işlemi sırasında da aynı delimiter kullanılıyor
            rows = list(reader)
            if len(rows) > 1:  # Eğer en az bir satır veri varsa
                last_row = rows[-1]
                deney_no = int(last_row[0]) + 1  # İlk sütun (deney_no) okunur ve artırılır
    
    # Yeni kayıt için verileri hazırla
    row = [
        deney_no, args.denek_, args.duration_, args.kayit_fps_,
        tekrar_index, args.tekrar_beklemesi_, args.delay_,
        args.cinsiyet_, args.mekan_, args.dcax_, args.dcay_, args.trgx_, args.trgy_
    ]
    
    # Yeni satırı dosyaya ekle
    with open(csv_file_path, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=';')  # Noktalı virgül ayırıcı burada da kullanılıyor
        writer.writerow(row)
