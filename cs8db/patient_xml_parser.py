import xml.etree.ElementTree as ET

from patient import Patient

class PatientXMLParser:

    @staticmethod
    def parse_patient_xml(xml_path):
        tree = ET.parse(xml_path)
        root = tree.getroot()

        patient_data = {}

        # Найдём тег <patient>
        patient = root.find('patient')
        if patient is not None:
            for param in patient.findall('parameter'):
                key = param.get('key')
                value = param.get('value')
                if key and value:
                    patient_data[key] = value
        else:
            print("⚠️ Тег <patient> не найден в XML.")

        return Patient(**patient_data)