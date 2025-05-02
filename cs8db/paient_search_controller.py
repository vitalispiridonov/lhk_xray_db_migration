from flask import Flask, jsonify, request
from cs8db_reporitory import Cs8DbRepository
from patient_xray_service import PatientXrayService

from patient_xray_service import PatientXrayService

app = Flask(__name__)

@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({'message': 'pong', 'status': 'ok'})

@app.route('/patients/search', methods=['GET'])
def get_patient():
    first_name = request.args.get("first_name")
    last_name = request.args.get("last_name")
    birth_date = request.args.get("birth_date")
    ssn = request.args.get("ssn")
    clinic_id = request.args.get("clinic_id")
    cabinet_nr = request.args.get("cabinet_nr")

    ip = request.remote_addr

    try:
        with Cs8DbRepository() as cs8db:
            cs8db.log_patient_search(first_name, last_name, birth_date, ssn, clinic_id, cabinet_nr, ip)
            patients = []
            for patient in cs8db.find_patients(first_name, last_name, ssn, birth_date):
                print(type(patient.date))
                patients.append({
                    'first_name': patient.first_name,
                    'last_name': patient.last_name,
                    'birth_date': patient.date.strftime('%Y-%m-%d'),
                    'ssn': patient.ssn,
                })
            return jsonify(patients)
    except Exception as e:
        print(e)

    return jsonify([])

@app.route('/clients', methods=['GET'])
def get_client():
    key = request.args.get("key")

    try:
        with Cs8DbRepository() as cs8db:
            client = cs8db.get_client_by_key(key)
            if client:
                return jsonify(client.to_dict())
            return jsonify({})
    except Exception as e:
        print(e)

    return jsonify({})

@app.route('/patients/xrays', methods=['GET'])
def get_patient_xrays():
    patient_ssn = request.args.get("patient_ssn")

    patient_service = PatientXrayService()
    xrays = patient_service.find_patients_xrays(patient_ssn)

    return jsonify([x.to_dict() for x in xrays])

@app.route('/patients/xrays/move', methods=['POST'])
def move_patient_xrays():
    source_patient_ssn = request.form.get('source_patient_ssn')
    target_patient_ssn = request.form.get('target_patient_ssn')
    xray_name = request.form.get('xray_name')

    is_verified = request.form.get('is_verified').lower() in ['true', '1', 'yes', 'on']
    xray_patient_ssn = request.form.get('xray_patient_ssn', '').strip()
    xray_patient_name = request.form.get('xray_patient_name', '').strip()

    patient_xray_service = PatientXrayService()

    if is_verified and xray_patient_ssn and xray_patient_name:
        patient_xray_service.move_xray(xray_name, source_patient_ssn, target_patient_ssn, xray_patient_ssn, xray_patient_name)
        return jsonify({'result': 'OK'})
    else:
        xray_patient_data = patient_xray_service.get_patient_info(target_patient_ssn)
        return jsonify({'result': 'VERIFICATION_REQUIRED', 'xray_patient_data': xray_patient_data})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
