import csv
from lhk_cs_migration_repository import CsMigrationRepository

def update_migration_id(input_file):
    with CsMigrationRepository() as cs_migration_repository:
        with open(input_file, mode='r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            print(reader.fieldnames)

            for row in reader:
                cs_migration_repository.update_migration_id(row['dicom_patient_id'], row['id'])

update_migration_id('./migration_id.csv')