from datetime import datetime

import chardet

class Patient:
    def __init__(self, dicom_patient_id, folder, first_name, last_name, date, ssn, photo, extnum, ssn_found):
        self.dicom_patient_id = dicom_patient_id
        self.folder = folder
        self.first_name = first_name
        self.last_name = last_name
        self.date = date
        self.ssn = ssn
        self.photo = photo
        self.extnum = extnum
        self.ssn_found = ssn_found

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
