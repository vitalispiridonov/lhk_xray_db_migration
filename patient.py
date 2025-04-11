from datetime import datetime

import chardet

class Patient:
    def __init__(self, dicom_patient_id=None, directory=None, first_name=None, last_name=None, birth_date=None,
                 ssn=None, photo=None, extnum=None, ssn_found=None, internal_id=None, sex=None):
        self.dicom_patient_id = dicom_patient_id
        self.folder = directory
        self.first_name = first_name
        self.last_name = last_name
        self.date = birth_date
        self.ssn = ssn
        self.photo = photo
        self.extnum = extnum
        self.ssn_found = ssn_found
        self.internal_id = internal_id
        self.sex = sex

    def __repr__(self):
        return (f"Patient"
                f"(NUMERO={self.dicom_patient_id}, "
                f"(FOLDER={self.folder}, "
                f"NOM={self.first_name}, "
                f"PRENOM={self.last_name}, "
                f"DATE={self.date}, "
                f"SECU={self.ssn}, "
                f"PHOTO={self.photo}, "
                f"EXTNUM={self.extnum}), "
                f"SSN_FOUND={self.ssn_found})")

    def compare_dats(self, patient):
        dates_same = True
        if self.date and patient.date:
            date1 = self.date
            if isinstance(date1, str):
                date1 = datetime.strptime(self.date, "%Y-%m-%d").date()

            date2 = patient.date
            if isinstance(date2, str):
                date2 = datetime.strptime(patient.date, "%Y-%m-%d").date()

        return dates_same

    def is_same(self, patient):
        dates_same = self.compare_dats(patient)
        print(f"Dates same: {dates_same}")


        res = (self.first_name == patient.first_name and
               self.last_name == patient.last_name and
               dates_same)

        if not res:
            print(f"Firstname: {self.first_name == patient.first_name}")
            print(f"Lastname: {self.last_name == patient.last_name}")

        return res


def convert_to_date(date_string):
    if not date_string:
        return ''

    try:
        date_object = datetime.strptime(date_string, "%Y%m%d")
        return date_object
    except ValueError:
        return ''


def check_secu(secu_value):
    secu_value = secu_value.strip()
    if secu_value:
        return "CSDB"
    else:
        return ""

def parse_patient_file(folder_path):
    patient_data = {}

    with open(folder_path + '\\FILEDATA.TXT', 'rb') as file:
        raw_data = file.read()
        encoding = chardet.detect(raw_data).get('encoding')

    with open(folder_path + '\\FILEDATA.TXT', 'r', encoding=encoding) as file:
        for line in file:
            line = line.strip()
            if '=' in line:
                key, value = line.split('=', 1)
                patient_data[key.strip()] = value.strip()

    patient = Patient(
        dicom_patient_id=patient_data.get('NUMERO', ''),
        folder=folder_path,
        first_name=patient_data.get('NOM', ''),
        last_name=patient_data.get('PRENOM', ''),
        date=convert_to_date(patient_data.get('DATE', '')),
        ssn=patient_data.get('SECU', ''),
        photo=patient_data.get('PHOTO', ''),
        extnum=patient_data.get('EXTNUM', ''),
        ssn_found = check_secu(patient_data.get('SECU', ''))
    )

    return patient
