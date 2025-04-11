from flask import Flask, jsonify, request
from cs8db_reporitory import Cs8DbRepository

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

if __name__ == '__main__':
    app.run(debug=True, port=5000)
