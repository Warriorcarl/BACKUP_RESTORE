import os
import tarfile
import zstandard as zstd
import psutil
import shutil
import time
import tempfile
from datetime import timedelta
from datetime import datetime

# Warna dan ikon
RESET = "\033[0m"
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
CHECK_ICON = "✅"
WARNING_ICON = "⚠️"
INFO_ICON = "ℹ️"
CLOCK_ICON = "⏰"
PROGRESS_ICON = "🔄"

# Folder data aplikasi
APP_FOLDERS = {
    "Google Chrome": os.path.expanduser(r'~\AppData\Local\Google\Chrome'),
    "Notepad++": os.path.expanduser(r'~\AppData\Roaming\Notepad++'),
}

# Folder umum (Dokumen, Desktop, dll.)
COMMON_FOLDERS = {
    "My Documents": os.path.expanduser(r'~\Documents'),
    "Desktop": os.path.expanduser(r'~\Desktop'),
    "My Pictures": os.path.expanduser(r'~\Pictures')
}

# Folder default yang dapat diatur pertama kali
default_backup_folder = None

def check_and_stop_processes(app_name):
    """Memeriksa dan menghentikan proses aplikasi jika berjalan"""
    processes_found = []
    for process in psutil.process_iter(['name', 'pid']):
        if app_name.lower() in process.info['name'].lower():
            processes_found.append(process)

    if processes_found:
        print(f"\n{YELLOW}{WARNING_ICON} {app_name} sedang berjalan.{RESET}")
        action = input(f"{YELLOW}Ingin menghentikan semua proses ini? (y/n): {RESET}").strip().lower()
        if action == 'y':
            for process in processes_found:
                process.terminate()
                process.wait()
            print(f"{GREEN}{CHECK_ICON} Semua proses {app_name} telah dihentikan.{RESET}")
            return True
        else:
            print(f"{RED}{WARNING_ICON} Proses backup dibatalkan.{RESET}")
            return False
    return True

def set_default_backup_folder():
    """Menentukan lokasi folder default untuk menyimpan backup"""
    global default_backup_folder
    default_backup_folder = input(f"{BLUE}{INFO_ICON} Masukkan lokasi default folder untuk menyimpan backup: {RESET}")
    if not os.path.exists(default_backup_folder):
        os.makedirs(default_backup_folder)
    print(f"{GREEN}{CHECK_ICON} Lokasi default folder backup disimpan: {default_backup_folder}{RESET}")

def get_backup_folder_path():
    """Meminta path folder untuk menyimpan backup dengan opsi default"""
    if default_backup_folder:
        print(f"{BLUE}{INFO_ICON} Lokasi default backup folder: {default_backup_folder}{RESET}")
        use_default = input("Ingin menggunakan lokasi default ini? (y/n): ").strip().lower()
        if use_default == 'y':
            return default_backup_folder
    return input(f"{BLUE}{INFO_ICON} Masukkan lokasi folder untuk menyimpan backup: {RESET}")

def generate_backup_filename(base_name):
    """Menghasilkan nama file backup dengan timestamp"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    return f"{base_name}_{timestamp}.zst"

def compress_folder(source_dir, backup_file):
    """Membackup folder dengan kompresi zstd dengan progress"""
    total_size = get_size(source_dir)
    start_time = time.time()

    print(f"{YELLOW}{PROGRESS_ICON} Backup dimulai untuk folder: {source_dir}{RESET}")
    dctx = zstd.ZstdCompressor(level=22)
    bytes_written = 0

    with open(backup_file, 'wb') as f_out:
        with dctx.stream_writer(f_out) as compressor_stream:
            with tarfile.open(fileobj=compressor_stream, mode='w') as tar:
                for root, _, files in os.walk(source_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        tarinfo = tar.gettarinfo(file_path)
                        tarinfo.size = os.path.getsize(file_path)
                        with open(file_path, 'rb') as f:
                            tar.addfile(tarinfo, fileobj=f)
                            bytes_written += tarinfo.size
                            display_progress(bytes_written, total_size, start_time)

    print(f"\n{GREEN}{CHECK_ICON} Backup selesai! File backup disimpan di: {backup_file}{RESET}")

def decompress_restore(backup_file, restore_dir):
    """Merestore file backup dengan dekompresi zstd dan progress"""
    dctx = zstd.ZstdDecompressor()
    start_time = time.time()

    # Step 1: Hitung ukuran total data hasil dekompresi
    with tempfile.TemporaryFile() as temp_file:
        with open(backup_file, 'rb') as f_in:
            decompressed_data = dctx.stream_reader(f_in)
            while True:
                chunk = decompressed_data.read(65536)
                if not chunk:
                    break
                temp_file.write(chunk)

        temp_file.seek(0)
        with tarfile.open(fileobj=temp_file, mode='r') as tar:
            total_size = sum(tarinfo.size for tarinfo in tar)

    # Step 2: Lakukan dekompresi dan ekstraksi dengan progress
    bytes_read = 0
    print(f"{YELLOW}{PROGRESS_ICON} Restore dimulai dari file: {backup_file}{RESET}")
    with tempfile.TemporaryFile() as temp_file:
        with open(backup_file, 'rb') as f_in:
            decompressed_data = dctx.stream_reader(f_in)
            while True:
                chunk = decompressed_data.read(65536)
                if not chunk:
                    break
                temp_file.write(chunk)
                bytes_read += len(chunk)
                display_progress(min(bytes_read, total_size), total_size, start_time)

            temp_file.seek(0)
            with tarfile.open(fileobj=temp_file, mode='r') as tar:
                tar.extractall(path=restore_dir, filter=lambda tarinfo, _: tarinfo)

    print(f"\n{GREEN}{CHECK_ICON} Restore selesai! File dikembalikan ke folder: {restore_dir}{RESET}")

def display_progress(current, total, start_time):
    """Menampilkan progress dalam persentase, waktu berjalan, dan estimasi waktu selesai"""
    elapsed_time = time.time() - start_time
    progress = current / total
    percent = progress * 100
    speed = current / elapsed_time if elapsed_time > 0 else 0
    remaining_time = (total - current) / speed if speed > 0 else 0

    print(f"\r{YELLOW}{PROGRESS_ICON} Progress: {percent:.2f}% | Waktu berjalan: {timedelta(seconds=int(elapsed_time))} "
          f"| Estimasi selesai: {timedelta(seconds=int(remaining_time))}{RESET}", end='')

def get_size(start_path):
    """Menghitung ukuran total folder"""
    total_size = 0
    for dirpath, _, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size

def backup_custom_paths():
    """Backup untuk beberapa custom path yang dimasukkan pengguna"""
    paths = []
    while True:
        path = input(f"{BLUE}{INFO_ICON} Masukkan path folder yang ingin dibackup (atau ketik 'done' untuk selesai): {RESET}")
        if path.lower() == 'done':
            break
        elif os.path.exists(path):
            paths.append(path)
        else:
            print(f"{RED}{WARNING_ICON} Path tidak ditemukan. Silakan coba lagi.{RESET}")

    backup_folder = get_backup_folder_path()
    for path in paths:
        folder_name = os.path.basename(path)
        backup_file = os.path.join(backup_folder, generate_backup_filename(folder_name))
        compress_folder(path, backup_file)

def restore_custom_path():
    """Restore custom path dari backup yang dipilih pengguna"""
    path = input(f"{BLUE}{INFO_ICON} Masukkan path folder untuk restore: {RESET}")
    backup_file = input(f"{BLUE}{INFO_ICON} Masukkan path file backup untuk restore ({os.path.basename(path)}): {RESET}")

    if os.path.exists(backup_file):
        if os.path.exists(path):
            renamed_folder = path + "_old"
            print(f"{YELLOW}{WARNING_ICON} Folder ditemukan, mengganti nama menjadi: {renamed_folder}{RESET}")
            shutil.move(path, renamed_folder)

        decompress_restore(backup_file, path)
    else:
        print(f"{RED}{WARNING_ICON} File backup tidak ditemukan.{RESET}")

def main_menu():
    global default_backup_folder
    while True:
        print(f"\n{BLUE}===== Menu Backup & Restore ====={RESET}")
        print("1. Set Lokasi Default Backup Folder")
        print("2. Backup Data Aplikasi")
        print("3. Restore Data Aplikasi")
        print("4. Backup Folder Umum")
        print("5. Restore Folder Umum")
        print("6. Backup Custom Path")
        print("7. Restore Custom Path")
        print("8. Keluar")
        pilihan = input(f"{BLUE}{INFO_ICON} Pilih opsi (1/2/3/4/5/6/7/8): {RESET}")

        if pilihan == "1":
            set_default_backup_folder()
        elif pilihan == "2":
            backup_data_app()
        elif pilihan == "3":
            restore_data_app()
        elif pilihan == "4":
            backup_common_folder()
        elif pilihan == "5":
            restore_common_folder()
        elif pilihan == "6":
            backup_custom_paths()
        elif pilihan == "7":
            restore_custom_path()
        elif pilihan == "8":
            print(f"{RED}{CLOCK_ICON} Keluar dari program.{RESET}")
            break
        else:
            print(f"{RED}{WARNING_ICON} Pilihan tidak valid. Silakan coba lagi.{RESET}")

def backup_data_app():
    while True:
        print(f"\n{BLUE}-- Pilih Aplikasi untuk Backup --{RESET}")
        for idx, app_name in enumerate(APP_FOLDERS.keys(), start=1):
            print(f"{idx}. {app_name}")
        print("0. Kembali")
        app_choice = int(input(f"{BLUE}{INFO_ICON} Pilih aplikasi: {RESET}"))

        if app_choice == 0:
            break
        app_name = list(APP_FOLDERS.keys())[app_choice - 1]
        app_folder = APP_FOLDERS[app_name]
        backup_folder = get_backup_folder_path()
        backup_file = os.path.join(backup_folder, generate_backup_filename(app_name))
        if check_and_stop_processes(app_name):
            compress_folder(app_folder, backup_file)

def restore_data_app():
    while True:
        print(f"\n{BLUE}-- Pilih Aplikasi untuk Restore --{RESET}")
        for idx, app_name in enumerate(APP_FOLDERS.keys(), start=1):
            print(f"{idx}. {app_name}")
        print("0. Kembali")
        app_choice = int(input(f"{BLUE}{INFO_ICON} Pilih aplikasi: {RESET}"))

        if app_choice == 0:
            break
        app_name = list(APP_FOLDERS.keys())[app_choice - 1]
        app_folder = APP_FOLDERS[app_name]
        backup_file = input(f"{BLUE}{INFO_ICON} Masukkan path file backup untuk restore ({app_name}): {RESET}")
        if os.path.exists(backup_file):
            decompress_restore(backup_file, app_folder)
        else:
            print(f"{RED}{WARNING_ICON} File backup tidak ditemukan.{RESET}")

def backup_common_folder():
    while True:
        print(f"\n{BLUE}-- Pilih Folder Umum untuk Backup --{RESET}")
        for idx, folder_name in enumerate(COMMON_FOLDERS.keys(), start=1):
            print(f"{idx}. {folder_name}")
        print("0. Kembali")
        folder_choice = int(input(f"{BLUE}{INFO_ICON} Pilih folder: {RESET}"))

        if folder_choice == 0:
            break
        folder_name = list(COMMON_FOLDERS.keys())[folder_choice - 1]
        folder_path = COMMON_FOLDERS[folder_name]
        backup_folder = get_backup_folder_path()
        backup_file = os.path.join(backup_folder, generate_backup_filename(folder_name))
        compress_folder(folder_path, backup_file)

def restore_common_folder():
    while True:
        print(f"\n{BLUE}-- Pilih Folder Umum untuk Restore --{RESET}")
        for idx, folder_name in enumerate(COMMON_FOLDERS.keys(), start=1):
            print(f"{idx}. {folder_name}")
        print("0. Kembali")
        folder_choice = int(input(f"{BLUE}{INFO_ICON} Pilih folder: {RESET}"))

        if folder_choice == 0:
            break
        folder_name = list(COMMON_FOLDERS.keys())[folder_choice - 1]
        folder_path = COMMON_FOLDERS[folder_name]
        backup_file = input(f"{BLUE}{INFO_ICON} Masukkan path file backup untuk restore ({folder_name}): {RESET}")
        if os.path.exists(backup_file):
            decompress_restore(backup_file, folder_path)
        else:
            print(f"{RED}{WARNING_ICON} File backup tidak ditemukan.{RESET}")

if __name__ == "__main__":
    main_menu()
