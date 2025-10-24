from flask import Blueprint, request, jsonify




api = Blueprint('api/v1', __name__)




@api.route('/cout_chauffage')
def cout_chauffage():

    value_1 = request.args.get('value1')
    value_2 = request.args.get('value2')
    value_3 = request.args.get('value3')

    # TODO: process value_1, value_2 and value_3 to get the data
    
    # dummy data
    data = {
        'inference_time_sec': 0.1,
        'result': {
            'prediction': {
                'cout_chauffage_eur': 20
            },
            'informations': {
                'adresse': "30 rue de la République, 69001 Lyon",
                'insee': 69123,
                'coordinates': {
                    'longitude': 34.564830,
                    'latitude': 4.586023
                }
            }
        }
    }

    response = jsonify(data)
    response.headers.add("Access-Control-Allow-Origin", "*")

    return response