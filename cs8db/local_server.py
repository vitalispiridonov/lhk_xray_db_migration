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

@app.route('/client', methods=['GET'])
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