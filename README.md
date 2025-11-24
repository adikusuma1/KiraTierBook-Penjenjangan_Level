# 📚 KiraTierBook Readable Level

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Next.js](https://img.shields.io/badge/Next.js-14-black.svg)](https://nextjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)

KiraTierBook Readable Level adalah aplikasi berbasis web yang menggunakan Kecerdasan Buatan (AI) untuk mengklasifikasikan jenjang buku secara otomatis berdasarkan standar Kemendikbudristek (SK 030/P/2022). Aplikasi ini dirancang untuk membantu guru, pustakawan, dan orang tua dalam menentukan kesesuaian buku bacaan bagi anak-anak dan siswa, mulai dari Pembaca Dini (Jenjang A) hingga Pembaca Mahir (Jenjang E).

<!-- (Opsional: Tambahkan screenshot aplikasi di sini nanti, simpan gambar di folder frontend/public dan ganti path di bawah) -->
![Aplikasi Screenshot](frontend/public/screenshot.png) <!-- Placeholder untuk screenshot -->

## ✨ Fitur Utama

- 🔍 **Pencarian Buku Otomatis**: Mencari metadata buku (judul, penulis, jumlah halaman, cover) menggunakan Google Books API.
- 👁️ **Analisis Visual AI**: Menggunakan Google Gemini 2.0 Flash (Vision) untuk "melihat" halaman buku dan menganalisis proporsi gambar vs teks.
- 🧠 **Klasifikasi Cerdas**: Menentukan jenjang (A, B1, B2, B3, C, D, E) berdasarkan aturan ketat Kemendikbud (jumlah kata, struktur kalimat, jenis paragraf).
- 🎨 **Visualisasi Jenjang**: Menampilkan simbol jenjang resmi (Bintang, Lingkaran, Segitiga, Kotak) dengan warna yang sesuai standar.
- 🖼️ **Cover Buku HD**: Menampilkan sampul buku resolusi tinggi untuk estetika yang lebih baik.

## 🛠️ Teknologi yang Digunakan (Tech Stack)

Proyek ini dibangun dengan arsitektur **Monorepo** yang memisahkan Frontend dan Backend.

### Frontend (Client-Side)
- **Framework**: Next.js 14 (React)
- **Styling**: Tailwind CSS
- **Komponen UI**: Shadcn/UI (Radix UI based)
- **Ikon**: Lucide React
- **HTTP Client**: Axios

### Backend (Server-Side)
- **Bahasa**: Python 3.10+
- **Framework API**: FastAPI
- **Server**: Uvicorn
- **AI Engine**: LangChain + Google Gemini API
- **Scraper**: Playwright (untuk mengambil screenshot halaman pratinjau buku)

## 🚀 Cara Menjalankan Proyek (Instalasi)

Ikuti langkah-langkah berikut untuk menjalankan aplikasi di komputer lokal Anda.

### Prasyarat
- Node.js (v18 ke atas)
- Python (v3.10 ke atas)
- Google Cloud API Key (Untuk Books API)
- Google AI Studio API Key (Untuk Gemini AI)

### 1. Clone Repositori
```bash
git clone https://github.com/username-anda/kiratierbook.git
cd kiratierbook
```

### 2. Setup Backend
Buka terminal baru, lalu masuk ke folder backend:
```bash
cd backend

# Buat Virtual Environment (Opsional tapi disarankan)
python -m venv venv

# Windows:
venv\Scripts\activate

# Mac/Linux:
source venv/bin/activate

# Install Dependencies
pip install -r requirements.txt

# Install Browser untuk Scraper
playwright install chromium
```

**Konfigurasi Environment Backend:**
Buat file `.env` di dalam folder `backend/` dan isi dengan kunci API Anda:
```env
# Dapatkan di https://aistudio.google.com/
GOOGLE_API_KEY=Isi_Kunci_Gemini_Anda_Disini

# Dapatkan di https://console.cloud.google.com/ (Aktifkan Books API)
GOOGLE_BOOKS_API_KEY=Isi_Kunci_Books_API_Anda_Disini
```

**Jalankan Server Backend:**
```bash
python run.py
```
Server akan berjalan di `http://127.0.0.1:8000`

### 3. Setup Frontend
Buka terminal baru (biarkan terminal backend tetap jalan), lalu masuk ke folder frontend:
```bash
cd frontend

# Install Dependencies
npm install

# Jalankan Server Frontend
npm run dev
```
Aplikasi akan berjalan di `http://localhost:3000`

## 📂 Struktur Direktori
```
kiratierbook/
├── backend/                # Kode Python (API & AI)
│   ├── app/
│   │   ├── main.py         # Entry point API
│   │   ├── models.py       # Struktur data (Pydantic)
│   │   └── services/       # Logika Bisnis
│   │       ├── ai_engine.py    # Otak AI (Prompting Gemini)
│   │       ├── google_books.py # Pencarian Metadata
│   │       └── scraper.py      # Pengambil Screenshot
│   ├── run.py              # Script runner server
│   ├── requirements.txt    # Daftar library Python
│   └── .env                # (File rahasia, jangan di-upload)
│
├── frontend/               # Kode Next.js (Tampilan)
│   ├── app/
│   │   └── page.tsx        # Halaman Utama
│   ├── components/         # Komponen UI (Button, Card, dll)
│   ├── public/             # Aset gambar statis
│   └── package.json        # Daftar library JS
│
└── README.md               # Dokumentasi Proyek
```

## 📖 Pedoman Penjenjangan (Referensi)

Aplikasi ini mengacu pada **SK Kepala BSKAP Kemendikbudristek Nomor 030/P/2022**:

| Jenjang | Target Pembaca          | Warna Simbol | Karakteristik Utama |
|---------|-------------------------|--------------|---------------------|
| A       | Pembaca Dini (PAUD)    | 🔴 Merah    | Gambar dominan, kalimat tunggal pendek. |
| B1-B3   | Pembaca Awal (SD Awal) | 🟣 Ungu     | Kalimat mulai bervariasi, gambar mendukung teks. |
| C       | Pembaca Semenjana (SD Tinggi) | 🔵 Biru  | Paragraf narasi penuh, gambar proporsional. |
| D       | Pembaca Madya (SMP)    | 🟢 Hijau    | Kalimat majemuk bertingkat, paragraf variatif. |
| E       | Pembaca Mahir (SMA/Dewasa) | 🟡 Kuning | Teks analitis/kritis, istilah teknis/ilmiah. |

## 🤝 Kontribusi

Proyek ini bersifat open-source. Jika Anda ingin berkontribusi:
1. Fork repositori ini.
2. Buat branch fitur baru (`git checkout -b fitur-baru`).
3. Commit perubahan Anda (`git commit -am 'Tambah fitur baru'`).
4. Push ke branch (`git push origin fitur-baru`).
5. Buat Pull Request.

## 📜 Lisensi

[MIT License](https://opensource.org/licenses/MIT)

---

💡 **Tips**: Pastikan untuk mengganti placeholder username di URL clone dengan username GitHub Anda yang sebenarnya.