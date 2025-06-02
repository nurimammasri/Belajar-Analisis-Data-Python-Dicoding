# 📌 Deskripsi Proyek

Selamat datang di dokumentasi proyek akhir untuk kelas **"Belajar Analisis Data dengan Python"** dari Dicoding Academy. Tujuan utama proyek ini adalah mengeksplorasi dataset penyewaan sepeda (Bike Sharing) dan membangun sebuah **dashboard interaktif** yang menyajikan informasi berbasis data dengan visualisasi yang menarik dan informatif.

Analisis berfokus pada identifikasi tren penggunaan sepeda berdasarkan waktu (jam, hari, musim), serta dampak cuaca terhadap pola penyewaan.

# 👤 Profil Pengembang

* **Nama:** Nur Imam Masri
* **Email:** [nurimammasri.01@gmail.com](mailto:nurimammasri.01@gmail.com)
* **ID Dicoding:** imammasri

# 📂 Struktur Folder

Struktur direktori yang disarankan untuk proyek ini:

```
bike-sharing-dashboard/
├── dashboard/
│   └── dashboard.py
├── data_clean/
│   ├── daily_bike_data.csv
│   └── hourly_bike_data.csv
├── notebook.ipynb
├── requirements.txt
└── README.md
```

> 📝 *Catatan: Jika Anda menyimpan file `.csv` di root folder, pastikan untuk menyesuaikan path di dalam skrip Python.*

# ⚙️ Panduan Setup Environment

## Opsi 1: Menggunakan Anaconda

```bash
conda create --name analisis-sepeda-dicoding python=3.9
conda activate analisis-sepeda-dicoding
pip install -r requirements.txt
```

## Opsi 2: Menggunakan Python Virtual Environment

```bash
# Buat direktori proyek
mkdir proyek_analisis_sepeda_dicoding
cd proyek_analisis_sepeda_dicoding

# Clone repositori (ganti URL-nya)
git clone [URL_REPOSITORI_ANDA]
cd [folder-repositori]

# Buat virtual environment
python -m venv env_sepeda

# Aktivasi environment
# Windows:
env_sepeda\Scripts\activate
# macOS/Linux:
source env_sepeda/bin/activate

# Instal dependensi
pip install -r requirements.txt
```

# 📦 Isi File `requirements.txt`

Berikut adalah contoh isi file dependensi Python yang digunakan:

```
streamlit
pandas
numpy
matplotlib
seaborn
```

Untuk menghasilkan file ini dari environment Anda:

```bash
pip freeze > requirements.txt
```

# 🚀 Menjalankan Aplikasi Dashboard

Setelah semua dependensi terinstal dan data siap, jalankan dashboard dengan:

```bash
cd dashboard
streamlit run dashboard.py
```

Aplikasi akan terbuka otomatis di browser Anda.

# 🔗 Tautan Deployment (Opsional)

Setelah Anda melakukan deploy ke platform seperti Streamlit Cloud, tambahkan tautan berikut:

**URL Dashboard Publik:**
👉 https\://\[tautan-dashboard-anda].streamlit.app/

Terima kasih telah membaca dokumentasi ini. Semoga proyek ini memberikan wawasan baru mengenai data penyewaan sepeda! 🚲📊
