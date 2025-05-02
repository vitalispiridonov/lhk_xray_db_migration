from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route('/patients/search', methods=['GET'])
def search_patients():
    patient = {
        'first_name': 'VADIM',
        'last_name': 'KUDRJAVTSEV',
        'birth_date': '1976-11-01',
        'ssn': '37611012241'
    }
    return jsonify([patient])

@app.route('/patients/xrays', methods=['GET'])
def get_patient_xrays():
    patient_ssn = request.args.get("patient_ssn")

    # Search patieng by ssn

    xrays = [
        {'name': 'VOL_1', 'type': '3D', 'date_time': '2024-11-01 14:50'},
        {'name': 'VOL_2', 'type': '3D', 'date_time': '2023-05-12 9:34'},
        {'name': 'c1', 'type': 'Crio', 'date_time': '2020-01-20 14:18'},
        {'name': 'c2', 'type': 'Crio', 'date_time': '2022-07-20 14:20'},
        {'name': 'p1', 'type': 'Pano', 'date_time': '2022-07-20 17:53'}
    ]

    return jsonify(xrays)

@app.route('/patients/xrays/move', methods=['POST'])
def move_patient_xray():
    source_patient_ssn = request.form.get('source_patient_ssn')
    target_patient_ssn = request.form.get('target_patient_ssn')
    xray_name = request.form.get('xray_name')

    is_verified = request.form.get('is_verified').lower() in ['true', '1', 'yes', 'on']
    patient_ssn = request.form.get('xray_patient_ssn', '').strip()
    patient_name = request.form.get('xray_patient_name', '').strip()

    if is_verified and patient_ssn and patient_name:
        # Move xray
        return jsonify({'result': 'OK'})
    else:
        xray_patient_data = {"ssn": target_patient_ssn, "name": "John Doe"}
        return jsonify({'result': 'VERIFICATION_REQUIRED', 'xray_patient_data': xray_patient_data})


@app.route('/clients', methods=['GET'])
def get_client():
    key = request.args.get("key")

    client = {
        "key": key,
        "cabinet_nr": "TEST-001",
        "clinic_id": 1,
        "type": "cab"
    }
    return jsonify(client)


app.run(debug=True, port=5000)