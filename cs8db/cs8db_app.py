from cs8db_reporitory import Cs8DbRepository
from patient_xml_parser import PatientXMLParser
from patient import Patient

import os

def find_patients(dir):
    directories = []
    for item in os.listdir(dir):
        directories.append(item)

    return directories

dbDir = "F:\\CS8DB"
dirs = find_patients(dbDir)

with Cs8DbRepository() as cs8db:
    for ssn in dirs:
        full_path = os.path.join(dbDir, ssn, "PatientInfo.xml")
        if os.path.isfile(full_path):
            try:
                patient = PatientXMLParser.parse_patient_xml(full_path)
                if not cs8db.is_patient_exists_by_ssn(ssn):
                    cs8db.create_patient(patient, ssn)
                else:
                    dbPatient = cs8db.get_patient_by_ssn(ssn)
                    if patient:
                        same = not patient.is_same(dbPatient)
                        if not same:
                            cs8db.update_patient(patient, ssn)
            except Exception as e:
                print(f"Exception with patient {ssn}")