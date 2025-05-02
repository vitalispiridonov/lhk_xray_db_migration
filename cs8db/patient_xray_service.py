import os
import datetime
import re
import shutil
import pydicom

from domain.patient import Patient
from domain.patient import parse_patient_file

from lhk_cs_migration_repository import CsMigrationRepository

class Xray:
    def __init__(self, name, type, date):
        self.name = name
        self.type = type
        self.date = date

    def to_dict(self):
        return {"name": self.name, "type": self.type, "date": self.date}


class PatientXrayService():


    def __init__(self):
        self.directory = "F:\\CS8DB"

    def find_patients_xrays(self, patientSsn):
        patient_directory = os.path.join(self.directory, patientSsn)

        xrays_list = []

        for xray_name in os.listdir(patient_directory):
            xray_path = os.path.join(patient_directory, xray_name)

            timestamp = os.path.getctime(xray_path)
            created_time = datetime.datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M")

            if (self.is_vol_folder(xray_name)):
                xrays_list.append(Xray(xray_name, "3D", created_time))

            if (self.is_crio(xray_name)):
                xrays_list.append(Xray(xray_name, "CRIO", created_time))

            if (self.is_pano(xray_name)):
                xrays_list.append(Xray(xray_name, "PANO", created_time))

        return xrays_list

    def move_xray(self, xray_name, source_patient_ssn, target_patient_ssn, xray_patient_ssn, xray_patient_name):
        target_patient_directory = os.path.join(self.directory, target_patient_ssn)

        with CsMigrationRepository() as cs_migration_repository:
            if self.is_vol_folder(xray_name):
                source_xray_directory = os.path.join(self.directory, source_patient_ssn, xray_name)
                target_xray_directory = os.path.join(self.directory, target_patient_ssn, xray_name)
                if os.path.exists(target_xray_directory):
                    new_folder_name = self.increment_folder_name(target_patient_directory)
                    new_xray_path = os.path.join(target_patient_directory, new_folder_name)
                    shutil.copytree(source_xray_directory, new_xray_path, xray_patient_ssn)
                    self.rename_dicom_3d_directory(target_patient_ssn, new_folder_name, xray_patient_ssn, xray_patient_name)
                    print(f'Директория {source_xray_directory} скопирована в {new_xray_path}')
                    cs_migration_repository.add_copied_file(source_xray_directory, new_xray_path, 1)
                else:
                    shutil.copytree(source_xray_directory, target_xray_directory)
                    self.rename_dicom_3d_directory(target_patient_ssn, xray_name, xray_patient_ssn, xray_patient_name)
                    print(f'Директория {source_xray_directory} скопирована в {target_xray_directory}')
                    cs_migration_repository.add_copied_file(source_xray_directory, target_patient_directory, 1)
            else:
                source_xray_file = os.path.join(self.directory, source_patient_ssn, xray_name)
                target_xray_file = os.path.join(self.directory, target_patient_ssn, xray_name)
                if (self.is_crio(target_xray_file) | self.is_pano(target_xray_file)):
                    if (os.path.exists(target_xray_file)):
                        new_name_path = self.increment_filename(target_xray_file, target_patient_directory)
                        shutil.copy2(source_xray_file, new_name_path)
                        self.rename_dicom_file(target_patient_ssn, os.path.basename(new_name_path), xray_patient_ssn, xray_patient_name)
                        print(f'Файл {source_xray_file} скопирован в {new_name_path}')
                        cs_migration_repository.add_copied_file(source_xray_file, new_name_path, 0)

                    else:
                        shutil.copy2(source_xray_file, target_xray_file)
                        self.rename_dicom_file(target_patient_ssn, os.path.basename(target_xray_file), xray_patient_ssn, xray_patient_name)
                        print(f'Файл {source_xray_file} скопирован в {target_xray_file}')
                        cs_migration_repository.add_copied_file(source_xray_file, target_xray_file, 0)

    def get_patient_info(self, ssn):
        patient_directory = os.path.join(self.directory, ssn)
        patient = parse_patient_file(patient_directory)

        return {'ssn': ssn, 'name': f'''{patient.last_name} {patient.first_name}'''}

    def is_crio(self, file_name):
        _, extension = os.path.splitext(file_name)

        return extension.lower() == '.crio'

    def is_pano(self, file_name):
        _, extension = os.path.splitext(file_name)

        return extension.lower() == '.pano'

    def is_vol_folder(self, folder_name):
        return folder_name.lower().startswith('vol')

    def increment_filename(self, file_name, target_dir):
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
            return self.increment_filename(new_file_name, target_dir)
        else:
            return new_file_name

    def increment_folder_name(self, target_dir):
        max_number = 0

        # Проходимся по всем папкам в целевой директории
        print
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

    def rename_dicom_file(self, target_patient_ssn, file_name, xray_patient_ssn, xray_patient_name):
        file_path = os.path.join(self.directory, target_patient_ssn, file_name)
        ds = pydicom.dcmread(file_path)
        patient_name = ds.get("PatientName", None)
        dicom_patient_name = '';
        if xray_patient_ssn.strip():
            dicom_patient_name = f'''{xray_patient_ssn.strip()}^'''

        dicom_patient_name += xray_patient_name

        ds.PatientName = dicom_patient_name
        ds.save_as(file_path)

    def rename_dicom_3d_directory(self, target_patient_ssn, directory_name, new_ssn, new_name):
        if self.is_vol_folder(directory_name):
            dicom_3d_directory_path = os.path.join(self.directory, target_patient_ssn, directory_name)
            for file_name in os.listdir(dicom_3d_directory_path):
                if file_name.endswith(".dcm"):
                    self.rename_dicom_file(dicom_3d_directory_path, file_name, new_ssn, new_name)


service = PatientXrayService()
#service.move_xray("VOL_1", "38705162215", "38705162215_TEST")
service.rename_dicom_3d_directory("38705162215_TEST", "VOL_1", "38705162216", "Vitali Spiridonov")
