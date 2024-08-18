import os
from database_manager import DatabaseManager

def get_folder_names(directory):
    # Получаем список всех элементов в директории
    items = os.listdir(directory)

    # Фильтруем список, оставляя только папки
    folders = [item for item in items if os.path.isdir(os.path.join(directory, item))]

    return folders


with DatabaseManager() as db_manager:
    directory_path = 'F:\\CS8DB'
    folder_names = get_folder_names(directory_path)
    for folder in folder_names:
        print(f"Найденная папка: {folder}")
        db_manager.update_done_by_ssn(folder, 1)