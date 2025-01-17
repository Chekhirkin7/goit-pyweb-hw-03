import os
import shutil
from pathlib import Path
import sys
import threading

def create_targer_dir (target_dir, extension): # створення підпапок з певними розширеннями
    ext_dir = target_dir / extension # створюється шлях де буде нова підпапка з певним розширенням
    ext_dir.mkdir(exist_ok = True) # створюється ця підпапка, якщо вона ще не створена
    return ext_dir # повертається шлях до цієї підпапки, для подальшого прийому даних, в неї будуть копіюватися дані

def copy_file (file, target_dir): # копіювання файлів в підпапки
    extension = file.suffix[1:].lower() # визначається розширення і по факту назва для папки
    if not extension: # якщо немає розширення у файла, то нічого не копіюємо
        return
    ext_dir = create_targer_dir(target_dir, extension) # викликаємо функцію для створення папок з новими аргументами, вже відомо звідки беруться аргументи
    shutil.copy2(file, ext_dir / file.name) # копіювання файлу з його метаданими, file - шлях до файлу, який копіюється, інший аргумент - шлях до папки в яку копіюється + назва файлу, яка в нього вже встановлена

def process_file (file, target_dir): # обгортка для функції копі файл, що забезпечує обробку винятків
    try:
        copy_file(file, target_dir) # пробуємо виконати
    except Exception as e:
        print(f"Помилка обробки файлу {file}: {e}") # якщо трапляється виняток

def process_directory (source_dir, target_dir): # шукаються всі файли в директорії
    threads = [] # зберігаються потоки
    for file in source_dir.rglob("*.*"): # пошук файлів з розширеннями
        if file.is_file(): # перевірка чи це є файлом
            thread = threading.Thread(target=process_file, args=(file, target_dir)) # створення потоку
            threads.append(thread) # додавання потоку в список
            thread.start() # запуск потоків

    for thread in threads: 
        thread.join() # об'єднання потоків, для коректності результату

def main():
    if len(sys.argv) < 2: # перевіряє кількість аргументів переданих в термінал
        print("Використання: python script.py <джерельна_директорія> [цільова_директорія]")
        return
    
    source_dir = Path(sys.argv[1]) # присвоюємо значення першого аргументу
    target_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("dist") # присвоюємо значення другого аргументу, якщо користувач його не дав, то за замовчуванням створиться папки діст у поточній директорії

    if not source_dir.is_dir():
        print("Джерельна директорія не існує або не є директорією.") # тут все і так зрозуміло
        return
    
    target_dir.mkdir(parents=True, exist_ok=True) # створює директорію куди будуть зберігатися файли і підпапки за вказаним шляхом parents=True: Якщо вказаний шлях містить декілька рівнів директорій, які ще не існують, цей параметр створює всі проміжні папки. другий параметр для контролю того, що папка вже створена, щоб не було винятка
    print(f"Обробка файлів з '{source_dir}' до '{target_dir}'...")
    process_directory(source_dir, target_dir) # запускаємо
    print("Обробка завершена.")

if __name__ == "__main__":
    main()
    current_dir_os = os.getcwd() # визначення поточного шляху директорії
    print(f"Поточна директорія (os): {current_dir_os}")

# Ці коментарі я написав для себе, для кращого розуміння, не звертайте уваги)