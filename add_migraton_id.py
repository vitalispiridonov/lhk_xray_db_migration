import csv
from database_manager import DatabaseManager

def update_migration_id(input_file):
    with DatabaseManager() as db_manager:
        with open(input_file, mode='r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            print(reader.fieldnames)

            for row in reader:
                db_manager.update_migration_id(row['dicom_patient_id'], row['id'])

update_migration_id('./migration_id.csv')