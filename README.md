# Aplikasi Resepsionis

Aplikasi Resepsionis adalah aplikasi berbasis Python yang digunakan untuk membantu proses administrasi penerimaan pasien di rumah sakit. Aplikasi ini terdiri dari dua komponen utama: backend dan desktop.

## 📦 Struktur Proyek

```
├── backend/               # Modul backend
│   └── main.py
│
├── desktop/               # Aplikasi desktop untuk resepsionis
│   ├── login.py
│   ├── show_patients.py
│   └── ...
│
├── data/                  # File database dummy & konfigurasi auth
│   ├── rs_harapan_bunda.db
│   ├── rs_sehat_sentosa.db
│   └── setupAuth.py
│
├── dist/                  # Hasil build .exe (tidak dipush ke repo)
│   └── AplikasiResepsionis.exe
│
├── build/                 # File hasil build (auto-generated)
│
├── AplikasiResepsionis.spec  # File spesifikasi PyInstaller
├── .gitignore
└── README.md
```

## ⚙️ Fitur Utama

- Autentikasi login resepsionis
- Menampilkan data pasien dari beberapa rumah sakit
- Pemindaian (scanner) untuk keperluan data masuk
- Aplikasi desktop dengan antarmuka pengguna sederhana
- Backend modular dan mudah dikembangkan

## 🖥️ Teknologi yang Digunakan

- Python 3.11
- SQLite (untuk penyimpanan data lokal)
- PyInstaller (untuk build .exe)
- Tkinter (kemungkinan untuk GUI Desktop)
- Modularisasi kode dengan struktur backend dan frontend (desktop)

## 🚀 Cara Menjalankan Aplikasi

### Jalankan Versi Development (langsung dari Python)

```bash
# Masuk ke folder desktop
cd desktop

# Jalankan aplikasi
python main.py
```

### Build Menjadi `.exe` dengan PyInstaller

```bash
pyinstaller --onefile --noconsole AplikasiResepsionis.spec
```

> Hasil build akan muncul di folder `dist/`.

## 📁 File yang Tidak Dipush

Beberapa file diabaikan dari repository untuk menjaga kebersihan dan keamanan:

- File build `.exe`
- File database `.db` asli
- Folder `__pycache__`
- File hasil kompilasi `.pyc`

## 🤝 Kontribusi

Jika kamu ingin berkontribusi, silakan fork repo ini dan ajukan pull request!

---

## 📜 Lisensi

Proyek ini dilisensikan di bawah lisensi MIT.
