import csv
from lhk_cs_migration_repository import CsMigrationRepository

def parse_patient_data(file_path):
    with CsMigrationRepository() as cs_migration_repository:
        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)

            for row in reader:
                patient_id = row['Patsient_ID']
                id_code = row['Isikukood']
                ssn_found = row['ssn_found']

                cs_migration_repository.add_ssn(patient_id, id_code, ssn_found)

                print(patient_id + ' ' + id_code + ' ' + ssn_found)

parse_patient_data('./no_ssn2.csv')