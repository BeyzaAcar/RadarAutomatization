RADAR PROJESİ
    Bu proje, radar ve kamera verilerini toplama, ön işleme, analiz etme ve görselleştirme için Python tabanlı bir sistemdir. Sistem modüler bir yapıya sahiptir ve belirli görevler için organize edilmiş scriptlerle çalışır. Bu modüler yapı, bakım ve genişletmeyi kolaylaştırır. Aşağıda projedeki tüm scriptlerin detaylı açıklamaları bulunmaktadır:

    1. auto_radar.py
        Amaç:
            Radar ve kamera verilerini senkronize bir şekilde toplar ve düzenli bir klasör yapısında saklar. Ayrıca, topladığı deney bilgilerini bir CSV dosyasına kaydeder.

        Ana İşlevler:
            Kamera Verisi Toplama: Bilgisayar kamerası ile video kaydı alır.
            Radar Verisi Toplama: Radar veri toplama işlemini tetikler ve dosyaları uygun klasöre taşır.
            Deney Bilgisi Güncelleme: Toplanan verilerle experiment_list.csv dosyasını günceller.
        Kullanım:
            Scripti çalıştırmadan önce, kodda geçen DCA ve Trigger noktalarının koordinatlarını manuel olarak ayarlayın (hard-coded).

        Çalıştırma:
            KOD:
                python auto_radar.py --denek_ <denek_id> --deney_no_ <deney_numarası> --duration_ <süre> --kayit_fps_ <fps> --tekrar_ <tekrar_sayısı> --tekrar_beklemesi_ <bekleme_süresi>
            Parametreler:
                --denek_: Denek adı veya ID'si.
                --deney_no_: Deney numarası.
                --duration_: Kamera kaydının süresi (saniye).
                --kayit_fps_: Kamera kaydının FPS değeri.
                --tekrar_: Kaç kez tekrar edileceği.
                --dcax_, --dcay_, --trgx_, --trgy_: Radar tetikleme noktalarının koordinatları (hard-coded).
            Notlar:
                * dcax_, dcay_, trgx_, trgy_ koordinatlarını gerektiğinde script içinde manuel olarak güncelleyin.
                * BinData ve CameraData dizin yollarının doğru olduğunu kontrol edin.

    2. csv_handler.py
        Amaç:
            experiment_list.csv dosyasını yönetir ve auto_radar.py tarafından toplanan deney bilgilerini kaydeder veya günceller.

        Ana İşlevler:
            Yeni bir deney kaydı oluşturur.
            Mevcut bir CSV dosyasını okur ve yeni verileri otomatik artan deney numarası ile ekler.
        Notlar:
        csv_file_path (varsayılan: experiment_list.csv) değerinin doğru ayarlandığından emin olun.
        CSV dosyasının formatını değiştirmeyin; aksi takdirde okuma/yazma hatası oluşabilir.
        Dosya mevcut değilse, script dosyayı otomatik olarak oluşturur.

    3. Ön İşleme Scriptleri
        Bu scriptler, ham radar verilerini analiz ve görselleştirme için hazırlar.

        3.1 dc_offset_removal.py
            Amaç:
                Ham radar .bin dosyalarından DC offset'i kaldırır ve işlenmiş veriyi .npy formatında kaydeder.

    Çalıştırma:

    KOD:
    python Preprocessing/dc_offset_removal.py
    Girdi:

    Dizin: Dataset/BinData/
    Dosya formatı: .bin
    Çıktı:

    Dizin: Dataset/ProcessedData/DCRemoved/
    Dosya formatı: .npy
    3.2 lowpass_filter.py
    Amaç:
    Radar verisine low-pass filtre uygular ve gürültüyü azaltır.

    Çalıştırma:


    KOD:
    python Preprocessing/lowpass_filter.py
    Girdi:

    Dizin: Dataset/ProcessedData/DCRemoved/
    Dosya formatı: _dc_removed.npy
    Çıktı:

    Dizin: Dataset/ProcessedData/Filtered/
    Dosya formatı: _filtered.npy
    3.3 fft_processing.py
    Amaç:
    Radar verisine Fast Fourier Transform (FFT) uygular ve range-Doppler haritaları oluşturur.

    Çalıştırma:


    KOD:
    python Preprocessing/fft_processing.py
    Girdi:

    Dizin: Dataset/ProcessedData/Filtered/
    Dosya formatı: _filtered.npy
    Çıktı:

    Dizin: Dataset/ProcessedData/FFT/
    Dosya formatı: _fft.npy
    3.4 microdoppler_stft.py
    Amaç:
    Short-Time Fourier Transform (STFT) kullanarak micro-Doppler spektrogramları oluşturur.

    Çalıştırma:


    KOD:
    python Preprocessing/microdoppler_stft.py
    Girdi:

    Dizin: Dataset/ProcessedData/FFT/
    Dosya formatı: _fft.npy
    Çıktı:

    Dizin: Dataset/ProcessedData/MicroDoppler/
    Dosya formatı: _microdoppler.npy
    3.5 angle_estimation.py
    Amaç:
    Radar verilerinden Angle of Arrival (AoA) değerlerini tahmin eder.

    Çalıştırma:


    KOD:
    python Preprocessing/angle_estimation.py
    Girdi:

    Dizin: Dataset/ProcessedData/FFT/
    Dosya formatı: _fft.npy
    Çıktı:

    Dizin: Dataset/ProcessedData/Angles/
    Dosya formatı: _angles.npy
    3.6 radar_to_pointcloud.py
    Amaç:
    Range, Doppler ve açı verilerini birleştirerek 3D nokta bulutları oluşturur.

    Çalıştırma:


    KOD:
    python Preprocessing/radar_to_pointcloud.py
    Girdi:

    Range verisi: Dataset/ProcessedData/FFT/
    Açı verisi: Dataset/ProcessedData/Angles/
    Çıktı:

    Dizin: Dataset/ProcessedData/PointCloud/
    Dosya formatı: _pointcloud.npy
    4. Görselleştirme Scriptleri
    Bu scriptler, işlenmiş radar verilerini analiz ve inceleme amacıyla görselleştirir.

    4.1 plot_range_doppler.py
    Amaç:
    Range-Doppler haritalarını görselleştirir.

    Çalıştırma:


    KOD:
    python Visualization/plot_range_doppler.py
    Girdi:

    Dizin: Dataset/ProcessedData/FFT/
    Dosya formatı: _fft.npy
    Çıktı:

    Dizin: Dataset/Visualizations/RangeDopplerPlots/
    Dosya formatı: .png
    4.2 plot_microdoppler.py
    Amaç:
    Micro-Doppler spektrogramlarını görselleştirir.

    Çalıştırma:


    KOD:
    python Visualization/plot_microdoppler.py
    Girdi:

    Dizin: Dataset/ProcessedData/MicroDoppler/
    Dosya formatı: _microdoppler.npy
    Çıktı:

    Dizin: Dataset/Visualizations/MicroDopplerPlots/
    Dosya formatı: .png
    4.3 plot_pointcloud.py
    Amaç:
    3D nokta bulutlarını görselleştirir.

    Çalıştırma:


    KOD:
    python Visualization/plot_pointcloud.py
    Girdi:

    Dizin: Dataset/ProcessedData/PointCloud/
    Dosya formatı: _pointcloud.npy
    Çıktı:

    Dizin: Dataset/Visualizations/PointCloudPlots/
    Dosya formatı: .png
    Genel Notlar
    Veri Yapısı: Girdi dizinlerinin (BinData, ProcessedData) doğru ayarlandığından emin olun.
    Parametre Ayarları: Low-pass filtresi veya FFT çözünürlüğü gibi parametreleri gerektiği gibi düzenleyin.
    Bağımlılıklar: Gerekli Python kütüphanelerini yüklemek için:

    KOD:
    pip install -r requirements.txt


PROJECT STRUCTURE

RadarProject/
    Preprocessing/                  # Scripts to prepare raw data for further use.
        dc_offset_removal.py        # Removes DC offset from raw radar data.
        lowpass_filter.py           # Applies low-pass filtering.
        fft_processing.py           # Performs FFT (range-Doppler).
        microdoppler_stft.py        # Extracts micro-Doppler signatures.
        angle_estimation.py         # Estimates angles using AoA methods.
        radar_to_pointcloud.py      # Converts processed radar data to point clouds.

    Visualization/                  # Scripts for visualizing processed data.
        plot_microdoppler.py        # Visualizes micro-Doppler spectrograms.
        plot_range_doppler.py       # Visualizes range-Doppler maps.
        plot_pointcloud.py          # Visualizes 3D point clouds.

    Modeling/                       # Scripts and models for analysis.
        clustering/
            dbscan_clustering.py    # Applies DBSCAN clustering on point clouds.
            kmeans_clustering.py    # Alternative clustering algorithm.
        classification/
            vgg16_training.py       # Trains micro-Doppler classification model.
            evaluation_metrics.py   # Evaluates classification performance.
        tracking/
            kalman_filter.py        # Object tracking using Kalman filter.

    Dataset/                        # Organized data storage.
        BinData/                    # Raw binary radar data.
        CameraData/                 # Corresponding camera data.
        ProcessedData/              # Outputs from preprocessing steps.
            DCRemoved/              # Data after DC offset removal.
            Filtered/               # Data after filtering.
            FFT/                    # FFT output (range-Doppler maps).
            MicroDoppler/           # Micro-Doppler spectrograms.
            PointCloud/             # Generated 3D point clouds.
        Visualizations/             # Outputs from visualization scripts.
            RangeDopplerPlots/      # Range-Doppler plots.
            MicroDopplerPlots/      # Micro-Doppler spectrograms.
            PointCloudPlots/        # 3D point cloud visualizations.

    venv/                           # Virtual environment for Python dependencies.
    requirements.txt                # Required Python libraries.
    README.md                       # Project overview and instructions.