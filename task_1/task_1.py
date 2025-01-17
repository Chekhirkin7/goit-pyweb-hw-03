import os
import shutil
from pathlib import Path
import sys
import threading

def create_targer_dir (target_dir, extension):
    ext_dir = target_dir / extension
    ext_dir.mkdir(exist_ok = True)
    return ext_dir

def copy_file (file, target_dir):
    extension = file.suffix[1:].lower()
    if not extension:
        return
    ext_dir = create_targer_dir(target_dir, extension)
    shutil.copy2(file, ext_dir / file.name)

def process_file (file, target_dir):
    try:
        copy_file(file, target_dir)
    except Exception as e:
        print(f"Помилка обробки файлу {file}: {e}")

def process_directory (source_dir, target_dir):
    threads = []
    for file in source_dir.rglob("*.*"):
        if file.is_file():
            thread = threading.Thread(target=process_file, args=(file, target_dir))
            threads.append(thread)
            thread.start()

    for thread in threads:
        thread.join()

def main():
    if len(sys.argv) < 2:
        print("Використання: python script.py <джерельна_директорія> [цільова_директорія]")
        return
    
    source_dir = Path(sys.argv[1])
    target_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("dist")

    if not source_dir.is_dir():
        print("Джерельна директорія не існує або не є директорією.")
        return
    
    target_dir.mkdir(parents=True, exist_ok=True)
    print(f"Обробка файлів з '{source_dir}' до '{target_dir}'...")
    process_directory(source_dir, target_dir)
    print("Обробка завершена.")

if __name__ == "__main__":
    main()
    current_dir_os = os.getcwd()
    print(f"Поточна директорія (os): {current_dir_os}")