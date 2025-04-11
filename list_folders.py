import os
from pathlib import Path

from patient import parse_patient_file
from lhk_cs_migration_repository import CsMigrationRepository


def get_subdirectories(directory):
    return [p.name for p in Path(directory).iterdir() if p.is_dir()]

with CsMigrationRepository() as cs_migration_repository:
    directory = 'F:\\CSDB'
    db_directory_names = get_subdirectories(directory)
    for db_directory_name in db_directory_names:
        db_directory = directory + '\\' + db_directory_name
        print(db_directory)
        patients_directory_names = get_subdirectories(db_directory)
        for patients_directory_name in patients_directory_names:
            patient_folder = db_directory + '\\' + patients_directory_name
            if os.path.exists(patient_folder + "\\FILEDATA.TXT"):
                patient = parse_patient_file(patient_folder)
                #print(patient)
                patient_exists = cs_migration_repository.is_patient_exists_by_dicom_patient_id(patient.dicom_patient_id)
                if not patient_exists:
                    print(f'New Patient {patient.dicom_patient_id}')
                    cs_migration_repository.add_patient(patient)