import pyodbc
from patient import Patient
from database_manager import DatabaseManager

server = 'WIN-5HQEEVML4E9\\CSISSERVER'
database = 'lhk-cs-migration'
username = 'test'
password = 'test'


class CsMigrationRepository:

    def __init__(self):
        self.dbManager = DatabaseManager(server, database, username, password)

    def add_patient(self, patient):
        try:
            insert_query = """
            INSERT INTO dbo.patients (dicom_patient_id, folder, ssn, first_name, last_name, birthday, done, created_at, updated_at, ssn_found)
            VALUES (?, ?, ?, ?, ?, ?, ?, GETDATE(), ?, ?)
            """
            self.dbManager.cursor.execute(insert_query, (
                patient.dicom_patient_id,
                patient.folder,
                patient.ssn,
                patient.first_name,
                patient.last_name,
                patient.date,
                0,
                None,
                patient.ssn_found,
            ))
            self.dbManager.connection.commit()
        except pyodbc.Error as e:
            print("Ошибка при выполнении запроса:", e)
            self.dbManager.connection.rollback()

    def find_patient_by_dicom_patient_id(self, dicom_patient_id):
        try:
            select_query = """
            SELECT * FROM dbo.patients WHERE dicom_patient_id = ?
            """
            self.dbManager.cursor.execute(select_query, (dicom_patient_id,))
            result = self.dbManager.cursor.fetchone()
            return result
        except pyodbc.Error as e:
            print("Ошибка при выполнении запроса:", e)
            return None

    def is_patient_exists_by_dicom_patient_id(self, dicom_patient_id):
        try:
            select_query = """
            SELECT CASE 
                WHEN EXISTS (
                    SELECT 1 
                    FROM dbo.patients 
                WHERE dicom_patient_id = ?
            ) 
            THEN 1 
            ELSE 0 
            END AS PatientExists;
            """
            self.dbManager.cursor.execute(select_query, (dicom_patient_id,))
            result = self.dbManager.cursor.fetchone()

            # Преобразование результата в True или False
            return bool(result.PatientExists)
        except pyodbc.Error as e:
            print("Ошибка при выполнении запроса:", e)
            return None

    def update_migration_id(self, dicom_patient_id, migration_id):
        try:
            update_migration_id_query = """
            UPDATE dbo.patients
            SET migration_id = ?
            WHERE dicom_patient_id = ?
            """
            self.dbManager.cursor.execute(update_migration_id_query, (migration_id, dicom_patient_id))
            self.dbManager.connection.commit()
        except pyodbc.Error as e:
            print("Ошибка при выполнении запроса:", e)
            return None

    def add_ssn(self, migration_id, ssn, ssn_found):
        try:
            update_migration_id_query = """
            UPDATE dbo.patients
            SET ssn = ?, 
            ssn_found = ?
            WHERE migration_id = ?
            """
            self.dbManager.cursor.execute(update_migration_id_query, (ssn, ssn_found, migration_id))
            self.dbManager.connection.commit()
        except pyodbc.Error as e:
            print("Ошибка при выполнении запроса:", e)
            return None

    def update_done(self, dicom_patient_id, done):
        try:
            update_done_query = """
            UPDATE dbo.patients
            SET done = ?,
            updated_at = GETDATE()
            WHERE dicom_patient_id = ?
            """
            self.dbManager.cursor.execute(update_done_query, (done, dicom_patient_id))
            self.dbManager.connection.commit()
        except pyodbc.Error as e:
            print("Ошибка при выполнении запроса:", e)
            return None

    def update_done_by_ssn(self, ssn, done):
        try:
            update_done_query = """
            UPDATE dbo.patients
            SET done = ?,
            updated_at = GETDATE()
            WHERE ssn = ?
            """
            self.dbManager.cursor.execute(update_done_query, (done, ssn))
            self.dbManager.connection.commit()
        except pyodbc.Error as e:
            print("Ошибка при выполнении запроса:", e)
            return None

    def find_not_done_patients(self):
        try:
            select_query = """
            SELECT * FROM dbo.patients WHERE done = 0
            """
            self.dbManager.cursor.execute(select_query)

            patients = []

            # Проход по результатам запроса и создание объектов Patient
            for row in self.dbManager.cursor.fetchall():
                patient = Patient(
                    dicom_patient_id=row.dicom_patient_id,
                    folder=row.folder,
                    first_name=row.first_name,
                    last_name=row.last_name,
                    date=row.birthday,
                    ssn=row.ssn,
                    photo='',
                    extnum='',
                    ssn_found=row.ssn_found,
                )
                patients.append(patient)

            # Закрытие соединения
            # self.dbManager.cursor.close()
            # self.dbManager.connection.close()

            return patients
        except pyodbc.Error as e:
            print("Ошибка при выполнении запроса:", e)
            return None

    def add_copied_file(self, from_folder, to, folder):
        try:
            insert_query = """
            INSERT INTO dbo.copied_files ([from], [to], folder)
            VALUES (?, ?, ?)
            """
            self.dbManager.cursor.execute(insert_query, (
                from_folder,
                to,
                folder
            ))
            self.dbManager.connection.commit()
        except pyodbc.Error as e:
            print("Ошибка при выполнении запроса:", e)
            self.dbManager.connection.rollback()
