import shutil
import os
import re
from database_manager import DatabaseManager

def copy_directory(source_dir, target_dir):
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    with DatabaseManager() as db_manager:
        for item in os.listdir(source_dir):
            # Полный путь к текущему элементу в исходной директории
            source_path = os.path.join(source_dir, item)
            # Полный путь к месту назначения
            target_path = os.path.join(target_dir, item).rstrip()

            if os.path.isdir(source_path):
                print(f'Copy directory {source_dir} to {target_dir}')
                if (os.path.exists(target_path)):
                    print(f'Директория существует {target_path}')
                    if is_vol_folder(item):
                        base_name, extension = os.path.splitext(source_path)
                        new_folder_name = increment_folder_name(base_name, target_dir)
                        #print(f'Новая имя папки {target_dir + "\\" + new_folder_name}')
                        shutil.copytree(source_path, target_dir + "\\" + new_folder_name)
                        db_manager.add_copied_file(source_path, target_dir +"\\" + new_folder_name, 1)
                else:
                    shutil.copytree(source_path, target_path)
                    print(f'Директория {source_path} скопирована в {target_path}')
                    db_manager.add_copied_file(source_path, target_path, 1)

            else:
                # Если это файл, копируем файл
                if (os.path.exists(target_path)):
                    #print(f'Файл существует {target_path}')
                    if is_crio_or_pano(target_path):
                        new_name = increment_filename(target_path, target_dir)
                        #print(f'Новое имя {new_name}')
                        shutil.copy2(source_path, new_name)
                        db_manager.add_copied_file(source_path, new_name, 0)

                else:
                    shutil.copy2(source_path, target_path)
                    #print(f'Файл {source_path} скопирован в {target_path}')
                    db_manager.add_copied_file(source_path, target_path, 0)

def increment_filename(file_name, target_dir):
    # Извлекаем имя файла и расширение
    base_name, extension = os.path.splitext(file_name)

    # Регулярное выражение для поиска числа в конце имени файла
    match = re.search(r'(\d+)$', base_name)

    if match:
        # Если число найдено, увеличиваем его
        number = int(match.group(1)) + 1
        base_name = re.sub(r'\d+$', str(number), base_name)
    else:
        # Если числа нет, добавляем 1 к имени файла
        base_name += '1'

    # Формируем новое имя файла
    new_file_name = base_name + extension

    # Проверяем, существует ли файл с таким именем в целевой директории
    if os.path.exists(os.path.join(target_dir, new_file_name)):
        # Рекурсивно увеличиваем число до тех пор, пока не найдем уникальное имя
        return increment_filename(new_file_name, target_dir)
    else:
        return new_file_name


def increment_folder_name(base_name, target_dir):
    max_number = 0

    # Проходимся по всем папкам в целевой директории
    for folder_name in os.listdir(target_dir):
        match = re.search(r'VOL_(\d+)$', folder_name)
        if match:
            number = int(match.group(1))
            #print(f'Папка: {folder_name} Номер: {number}')
            if number > max_number:
                max_number = number

    # Увеличиваем найденный максимальный номер на 1
    next_number = max_number + 1
    return f"VOL_{next_number}"



def check_path(string):
    return not string.strip() or string.strip() == "-"


def is_crio_or_pano(file_name):
    _, extension = os.path.splitext(file_name)

    return extension.lower() in ['.crio', '.pano']

def is_vol_folder(folder_name):
    return folder_name.lower().startswith('vol')


#copy_directory("F:\\CSDB\\P.RVG\\P0005376", "F:\\CS8DB\\310183-12953")

with DatabaseManager() as db_manager:
    patients = db_manager.find_not_done_patients()
    for patient in patients:
        if not check_path(patient.ssn):
            target_dir = 'F:\\CS8DB\\' + patient.ssn.strip()
            print(f'Copying {patient.folder} to {target_dir}')
            copy_directory(patient.folder, target_dir.strip())
            db_manager.update_done(patient.dicom_patient_id, 1)


