# Bot Backup & Restore

Bot ini adalah skrip Python untuk membackup dan merestore data aplikasi, folder umum, serta custom path dengan kompresi **Zstandard (zst)** dan pembagian file besar menjadi beberapa bagian (chunk). Skrip ini mendukung tampilan berwarna dan ikon untuk memberikan pengalaman pengguna yang lebih baik.

## Fitur Bot

- **Backup dan Restore Data Aplikasi**: Dapat melakukan backup dan restore untuk aplikasi tertentu seperti Google Chrome, Notepad++, dll.
- **Backup dan Restore Folder Umum**: Mendukung backup folder umum seperti My Documents, Desktop, dll.
- **Backup dan Restore Custom Path**: Pengguna dapat memasukkan beberapa custom path untuk dibackup dan direstore.
- **Pemisahan File Backup**: File backup besar secara otomatis dipisah menjadi beberapa bagian (chunk) dengan ukuran maksimal yang ditentukan.
- **Progress Bar dan Estimasi Waktu**: Menampilkan progress backup dan restore, termasuk persentase, estimasi waktu selesai, dan waktu proses berjalan.
- **Pemeriksaan Proses Aplikasi**: Memastikan aplikasi yang akan dibackup sudah berhenti sebelum memulai backup.

## Panduan Instalasi Python

### Windows

1. **Unduh Python**: Buka [Python.org](https://www.python.org/downloads/windows/) dan unduh versi terbaru Python untuk Windows.
2. **Instal Python**:
   - Buka file yang telah diunduh.
   - Centang opsi **Add Python to PATH** agar Python dapat diakses dari terminal.
   - Klik **Install Now** dan ikuti instruksi hingga selesai.
3. **Verifikasi Instalasi**:
   - Buka Command Prompt dan ketik:
     ```bash
     python --version
     ```
   - Pastikan versi Python muncul, yang menandakan Python sudah terinstal.

### Linux

1. **Periksa Instalasi Python**: Kebanyakan distro Linux sudah dilengkapi dengan Python. Untuk memeriksa versi, buka terminal dan ketik:
   ```bash
   python3 --version
   ```
2. **Instal Python (Jika Belum Ada)**:
   - Pada Ubuntu/Debian:
     ```bash
     sudo apt update
     sudo apt install python3
     ```
   - Pada CentOS/Fedora:
     ```bash
     sudo yum install python3
     ```

3. **Verifikasi Instalasi**:
   ```bash
   python3 --version
   ```

## Panduan Instalasi Modul Python

Bot ini membutuhkan beberapa modul Python. Instalasi modul-modul ini dapat dilakukan dengan **pip**.

1. **Pastikan pip sudah terinstal**:
   - Pada Windows, pip terinstal secara otomatis bersama Python.
   - Pada Linux, Anda bisa menginstalnya dengan:
     ```bash
     sudo apt install python3-pip
     ```

2. **Instal Modul yang Dibutuhkan**:
   Buka terminal atau command prompt dan jalankan perintah berikut untuk menginstal modul:
   ```bash
   pip install psutil zstandard
   ```

## Panduan Menjalankan Bot

1. **Clone Repository**: Jika bot disimpan di GitHub, clone repository dengan perintah:
   ```bash
   git clone https://github.com/username/bot-backup-restore.git
   ```
   Gantilah `username` dengan nama pengguna GitHub Anda.

2. **Navigasi ke Folder Bot**:
   ```bash
   cd bot-backup-restore
   ```

3. **Jalankan Bot**:
   - Pada Windows:
     ```bash
     python bot_backup_restore.py
     ```
   - Pada Linux:
     ```bash
     python3 bot_backup_restore.py
     ```

4. **Mengikuti Panduan Bot**:
   Saat bot dijalankan, ikuti instruksi pada layar untuk memilih jenis backup atau restore yang diinginkan, seperti backup aplikasi, folder umum, atau custom path. Bot akan menampilkan progress, waktu yang sudah berjalan, dan estimasi waktu selesai selama proses berlangsung.

## Catatan

- **Pengaturan Ukuran Chunk**: Ukuran maksimum setiap bagian (chunk) backup diatur dalam variabel `MAX_CHUNK_SIZE` pada skrip bot. Standarnya adalah **10GB** per chunk. Anda dapat mengubah ukuran ini sesuai kebutuhan.
