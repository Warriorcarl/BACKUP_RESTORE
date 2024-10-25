# Bot Backup & Restore

Bot ini adalah skrip Python untuk melakukan backup dan restore data aplikasi, folder umum, serta custom path menggunakan kompresi **Zstandard (zst)** dan mendukung pembagian file besar menjadi beberapa bagian (chunk). Skrip ini juga memiliki tampilan berwarna dan progress bar untuk memberikan pengalaman pengguna yang lebih baik.

## Fitur Bot

- **Backup dan Restore Data Aplikasi**: Mendukung backup dan restore untuk aplikasi seperti Google Chrome, Notepad++, dan lainnya.
- **Backup dan Restore Folder Umum**: Mendukung backup untuk folder umum seperti My Documents, Desktop, My Pictures, dan lainnya.
- **Backup dan Restore Custom Path**: Pengguna dapat memasukkan beberapa path custom untuk di-backup dan di-restore.
- **Pemisahan File Backup**: File backup besar secara otomatis dipecah menjadi beberapa bagian (chunk) dengan ukuran maksimum yang ditentukan.
- **Progress Bar dan Estimasi Waktu**: Menampilkan progress backup dan restore, termasuk persentase, estimasi waktu selesai, dan waktu proses berjalan.
- **Pemeriksaan Proses Aplikasi**: Memastikan aplikasi yang akan di-backup telah dihentikan sebelum backup dimulai.
- **Pengaturan Lokasi Default Backup**: Pengguna dapat menentukan lokasi default untuk menyimpan file backup, dan tidak perlu memasukkan ulang di setiap operasi.

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
   - Pastikan versi Python muncul, menandakan Python sudah terinstal.

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

4. **Penggunaan Bot**:
   - **Backup Data Aplikasi**: Pilih aplikasi yang ingin Anda backup dari daftar yang tersedia.
   - **Restore Data Aplikasi**: Pilih aplikasi yang ingin direstore dari file backup.
   - **Backup Folder Umum**: Pilih folder umum seperti My Documents atau Desktop untuk dibackup.
   - **Restore Folder Umum**: Pilih folder umum yang ingin direstore dari file backup.
   - **Backup Custom Path**: Masukkan satu atau beberapa path custom yang ingin dibackup.
   - **Restore Custom Path**: Masukkan path folder yang ingin direstore dan file backup-nya.

5. **Lokasi Backup Default**:
   - Pada menu utama, Anda bisa mengatur lokasi default untuk menyimpan file backup. Pengaturan ini akan digunakan di operasi berikutnya tanpa perlu menanyakan ulang lokasi.

## Catatan

- **Pengaturan Ukuran Chunk**: Ukuran maksimum setiap bagian (chunk) backup diatur dalam variabel `MAX_CHUNK_SIZE` pada skrip bot. Standarnya adalah **10GB** per chunk. Anda dapat mengubah ukuran ini sesuai kebutuhan.
- **Nama File dengan Timestamp**: File backup akan memiliki nama yang mencakup timestamp (waktu backup) untuk memastikan nama file selalu unik.

Jika Anda memiliki pertanyaan atau masalah terkait penggunaan bot, silakan buat issue di repository GitHub ini.

Selamat mencoba!
