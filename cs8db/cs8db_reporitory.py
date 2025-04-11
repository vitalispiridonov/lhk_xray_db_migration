from database_manager import DatabaseManager
import pyodbc

from patient import Patient

from patient_xml_parser import PatientXMLParser


server = 'WIN-5HQEEVML4E9\\CSISSERVER'
database = 'lhk-cs8db'
username = 'cs8db'
password = '9ShkXw1Y9aAx'


class Cs8DbRepository():

    def __init__(self):
        self.cs8db = DatabaseManager(server, database, username, password)

        with self.cs8db as db:
            db.cursor.execute("SELECT 1")

    def __enter__(self):
        self.cs8db.__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cs8db.__exit__(exc_type, exc_val, exc_tb)
        pass

    def is_patient_exists_by_ssn(self, dicom_patient_id):
        try:
            select_query = """
            SELECT CASE 
                WHEN EXISTS (
                    SELECT 1 
                    FROM dbo.patients 
                WHERE ssn = ?
            ) 
            THEN 1 
            ELSE 0 
            END AS PatientExists;
            """
            self.cs8db.cursor.execute(select_query, (dicom_patient_id,))
            result = self.cs8db.cursor.fetchone()

            # Преобразование результата в True или False
            return bool(result.PatientExists)
        except pyodbc.Error as e:
            print("Ошибка при выполнении запроса:", e)
            return None

    def is_patient_changed(self, ssn, first_name, last_name, date):
        try:
            select_query = """
            SELECT CASE 
                WHEN EXISTS (
                    SELECT 1 
                    FROM dbo.patients 
                WHERE ssn = 
            ) 
            THEN 1 
            ELSE 0 
            END AS PatientExists;
            """
            self.cs8db.cursor.execute(select_query, (dicom_patient_id,))
            result = self.cs8db.cursor.fetchone()

            # Преобразование результата в True или False
            return bool(result.PatientExists)
        except pyodbc.Error as e:
            print("Ошибка при выполнении запроса:", e)
            return None

    def create_patient(self, patient, ssn):
        try:
            create_query = """
                    INSERT INTO patients (
                        internal_id,
                        directory,
                        first_name,
                        last_name,
                        birth_date,
                        sex,
                        ssn,
                        created_at
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, GETDATE())
                """
            self.cs8db.cursor.execute(create_query, (
                    patient.internal_id,
                    patient.folder,
                    patient.first_name,
                    patient.last_name,
                    patient.date,
                    patient.sex,
                    ssn
                ))
            self.cs8db.connection.commit()
            print("✅ Пациент успешно добавлен.")
        except pyodbc.Error as e:
            print("❌update whe add patient:", e)

    def update_patient(self, patient, ssn):
        try:
            update_query = """
                    UPDATE patients
                        SET
                            first_name = ?,
                            last_name = ?,
                            birth_date = ?
                        WHERE
                            ssn = ?;
                """
            self.cs8db.cursor.execute(update_query, (
                    patient.first_name,
                    patient.last_name,
                    patient.date,
                    ssn
                ))
            self.cs8db.connection.commit()
        except pyodbc.Error as e:
            print("❌ Error when update patient:", e)

    def get_patient_by_ssn(self, ssn):
        try:
            select_query = """
                    SELECT 
                        id,
                        internal_id,
                        directory,
                        first_name,
                        last_name,
                        birth_date,
                        sex,
                        ssn,
                        created_at
                    FROM patients
                    WHERE ssn = ?
                """
            self.cs8db.cursor.execute(select_query, (ssn,))
            row = self.cs8db.cursor.fetchone()
            if row:
                return  Patient(
                        None,
                        row.directory,
                        row.first_name,
                        row.last_name,
                        row.birth_date,
                        row.ssn,
                        None,
                        None,
                        None,
                        row.internal_id,
                        row.sex
                    )

            else:
                return None
        except pyodbc.Error as e:
            print("❌ Ошибка при поиске пациента:", e)
            return None
