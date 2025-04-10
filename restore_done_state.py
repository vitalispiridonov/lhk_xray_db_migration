import os
from lhk_cs_migration_repository import CsMigrationRepository

def get_folder_names(directory):
    # Получаем список всех элементов в директории
    items = os.listdir(directory)

    # Фильтруем список, оставляя только папки
    folders = [item for item in items if os.path.isdir(os.path.join(directory, item))]

    return folders


with CsMigrationRepository() as cs_migration_repository:
    directory_path = 'F:\\CS8DB'
    folder_names = get_folder_names(directory_path)
    for folder in folder_names:
        print(f"Найденная папка: {folder}")
        cs_migration_repository.update_done_by_ssn(folder, 1)