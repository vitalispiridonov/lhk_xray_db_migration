import os

import pydicom

dir3d = "F:\\CS8DB\\60404010285\\VOL_1"
for filename in os.listdir(dir3d):
    if filename.endswith(".dcm"):
        path = os.path.join(dir3d, filename)
        ds = pydicom.dcmread(path)
        patient_name = ds.get("PatientName", "Не указано")
        print("Patient Name:", patient_name)
        ds.PatientName = "60404010285^Angelina Samoylova"
        ds.save_as(path)