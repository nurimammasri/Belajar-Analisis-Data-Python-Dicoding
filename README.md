# 📝 Ringkasan Proyek

Ini adalah dokumentasi proyek akhir dari kelas **Belajar Analisis Data dengan Python** yang diselenggarakan oleh Dicoding Academy. Proyek ini mengeksplorasi data bike sharing dan menyajikan hasil analisis dalam bentuk **dashboard interaktif** menggunakan Streamlit. Analisis bertujuan untuk memahami perilaku pengguna bike berdasarkan waktu (harian, musiman, jam), serta pengaruh cuaca terhadap frekuensi penyewaan.

---

# 👨‍💻 Tentang Pengembang

- **Nama:** Nur Imam Masri  
- **Email:** [nurimammasri.01@gmail.com](mailto:nurimammasri.01@gmail.com)  
- **ID Dicoding:** imammasri  

---

# 📁 Organisasi Proyek

Struktur folder yang digunakan dalam proyek ini disusun agar memudahkan pengelolaan data, notebook, dan deployment dashboard.

```

bike-sharing-dashboard/                  # Direktori utama proyek dashboard analisis data bike sharing
│
├── dashboard/                           # Folder untuk file dashboard Streamlit dan data siap visualisasi
│   ├── dashboard.py                     # Script utama Streamlit untuk menampilkan dashboard interaktif
│   ├── dashboard_main_data_day.csv      # Data harian hasil preprocessing untuk dashboard
│   └── dashboard_main_data_hour.csv     # Data per jam hasil preprocessing untuk dashboard
│
├── data/                                # Folder berisi data mentah (raw data)
│   ├── day.csv                          # Dataset agregasi harian penggunaan bike
│   └── hour.csv                         # Dataset agregasi per jam penggunaan bike
│
├── notebook.ipynb                       # Jupyter Notebook untuk EDA dan preprocessing data
├── requirements.txt                     # Daftar pustaka Python yang dibutuhkan untuk menjalankan proyek
├── README.md                            # Dokumentasi utama proyek (deskripsi, setup, cara pakai)
├── url.txt                              # Tautan ke dashboard online atau referensi lain (opsional)
└── .gitattributes                       # File konfigurasi Git terkait atribut file dalam repositori


````

> 🔍 **Catatan:** Jika Anda menempatkan file `.csv` di direktori utama, jangan lupa sesuaikan path pada script Python Anda.

---

# ⚙️ Panduan Instalasi dan Lingkungan

## 💼 Opsi 1: Anaconda (Direkomendasikan)

```bash
# Membuat environment baru
conda create --name bike-analysis-dicoding python=3.9

# Aktivasi environment
conda activate bike-analysis-dicoding

# Instalasi dependensi
pip install -r requirements.txt
````

## 🧪 Opsi 2: Virtual Environment Biasa

```bash
# Buat folder proyek dan masuk ke dalamnya
mkdir bike_analysis_dicoding
cd bike_analysis_dicoding

# Clone repository Anda
git clone [URL_REPOSITORI_ANDA]
cd [folder-repo-anda]

# Membuat virtual environment
python -m venv env

# Aktifkan environment
# Windows
env\Scripts\activate
# macOS/Linux
source env/bin/activate

# Instalasi dependensi
pip install -r requirements.txt
```

---

# 📄 Daftar Paket Python

Gunakan file `requirements.txt` untuk mendefinisikan dependensi proyek Anda. Contoh isi file:

```
streamlit
pandas
numpy
matplotlib
seaborn
```

Buat file ini dari environment aktif Anda dengan:

```bash
pip freeze > requirements.txt
```

---

# 🖥️ Menjalankan Dashboard

Setelah semua persiapan selesai dan data tersedia:

```bash
cd dashboard
streamlit run dashboard.py
```

Dashboard akan terbuka otomatis di browser default Anda.

---

# 🌐 Deployment Online

Setelah deploy ke Streamlit Community Cloud (atau platform lain), Anda dapat menambahkan tautan ke dashboard di bawah ini:

* **Link Aplikasi Streamlit:** [https://bikesharing-pad.streamlit.app](https://bikesharing-pad.streamlit.app)

---

# 🎉 Penutup

Proyek ini bertujuan untuk memberikan gambaran bagaimana analisis data dapat digunakan untuk mengidentifikasi pola penggunaan bike berbasis waktu dan cuaca. Semoga hasil yang ditampilkan melalui dashboard dapat memberi wawasan berharga bagi para pemangku kepentingan atau pengguna umum yang tertarik dengan mobilitas berkelanjutan.

Terima kasih telah mengikuti proyek ini! 🚴‍♂️📊