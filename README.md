RADAR PROJECT
    Bu proje, radar ve kamera verisi toplama, radar verisini işleme ve analiz etmeyi amaçlayan bir Python tabanlı sistemdir. Sistem, üç temel script ile çalışmaktadır:

1. auto_radar.py
    Amaç:
        Radar ve kamera verisini eş zamanlı olarak toplar ve bu verileri belirli bir klasör yapısında kaydeder. Ayrıca topladığı deney bilgilerini bir CSV dosyasına yazar.

    Temel İşlevler:
        * Kamera Verisi Toplama: Bilgisayar kamerasını kullanarak video kaydı alır ve kaydeder.
        * Radar Verisi Toplama: Radar tetikleme noktalarına tıklayarak radar verisini başlatır ve kaydedilen dosyayı belirli bir klasöre taşır.
        * Deney Bilgisi Güncelleme: Toplanan verilerle deney_list.csv dosyasını günceller.
        Kullanım:
        * Komutu çalıştırmadan önce kodda geçen koordinatları (DCA ve Trigger noktaları) elle ayarlamalısınız.

    ÇALIŞTIRMA:
    python auto_radar.py --denek_ <denek_id> --deney_no_ <deney_numarasi> --duration_ <sure> --kayit_fps_ <fps> --tekrar_ <tekrar_sayisi> --tekrar_beklemesi_ <bekleme_suresi>

    Parametreler:
    --denek_: Denek adı veya ID'si.
    --deney_no_: Deney numarası.
    --duration_: Kamera kaydının süresi (saniye).
    --kayit_fps_: Kamera kaydının FPS değeri.
    --tekrar_: Kaç kez tekrarlanacağı.
    --dcax_, --dcay_, --trgx_, --trgy_: Radar tetikleme noktalarının koordinatları (hard-coded).

2. csv_handler.py
    Amaç:
    auto_radar.py tarafından oluşturulan deney bilgilerini deney_list.csv dosyasına kaydeder veya günceller.

    Temel İşlevler:
        Yeni bir deney kaydı oluşturur.
        Mevcut bir CSV dosyasını okur ve deney numarasını otomatik artırarak yeni veriyi ekler.
        Dikkat Edilmesi Gerekenler:
        csv_file_path: CSV dosyasının adını ve yolunu elle kontrol edin. Varsayılan olarak deney_list.csv dosyasını kullanır.
        CSV'nin formatını değiştirmeyin. Aksi halde yazma/okuma hatası alabilirsiniz.

3. radar_processing.py
    Amaç:
        Ham radar verilerini (.bin dosyaları) alır, bunları filtreler, Fourier dönüşümü uygular ve işlenmiş veriyi .npy formatında kaydeder.

    Temel İşlevler:
        Ham radar verisine low-pass filtre uygular.
        Veriyi Fourier dönüşümü ile frekans alanına taşır.
        İşlenmiş veriyi ProcessedData klasörüne .npy formatında kaydeder.
        Kullanım:
        Bu script, Dataset/BinData/ klasöründeki tüm .bin dosyalarını otomatik olarak işler ve işlenmiş veriyi Dataset/ProcessedData/ klasörüne kaydeder.

    ÇALIŞTIRMA:
    python Radar/radar_processing.py


DİKKAT EDİLMESİ GEREKENLER

    auto_radar.py:

        DCA ve Trigger tıklama noktalarının koordinatları (örneğin, --dcax_, --dcay_, --trgx_, --trgy_) kod içinde hard-coded olarak ayarlanmıştır. Bu koordinatları manuel olarak değiştirmelisiniz.
        Dosya yollarını (BinData ve CameraData) kontrol ederek deney kayıtlarının doğru klasörlere kaydedildiğinden emin olun.

    csv_handler.py:

        deney_list.csv dosyasının formatını değiştirmeyin.
        Dosya mevcut değilse script otomatik oluşturur. Ancak, var olan bir dosyada eksik veya bozuk bir format varsa hata verebilir.

    radar_processing.py:

        İşlenecek .bin dosyaları Dataset/BinData/ klasöründe olmalıdır.
        Çıktı dosyaları Dataset/ProcessedData/ klasörüne kaydedilecektir.
        Eğer filtreleme veya Fourier dönüşümü için farklı parametreler kullanmak isterseniz, kodda butter_lowpass_filter fonksiyonundaki cutoff veya fs gibi değerleri değiştirmeniz gerekebilir.