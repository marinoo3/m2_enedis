from flask import Blueprint, request, jsonify, current_app




api = Blueprint('api/v1', __name__)



# Decorator factory function
def check_arguments(model:str):
    def decorator(f):
        def wrapper(*args, **kwargs):

            values = request.args.to_dict()
            features:dict = current_app.models.get_features(model)

            # Replace variables that will be computed later on
            features['annee_construction'] = features.pop('periode_construction')
            features['altitude'] = features.pop('classe_altitude')

            if values.keys() != features.keys():
                return jsonify({'error': "Missing or incorrect request parameters"})
            
            return f(*args, **kwargs)
        return wrapper
    return decorator






@api.route('/cout_chauffage')
@check_arguments('cout')
def cout_chauffage():

    values = request.args.to_dict()
    # convert to numeric
    values['annee_construction'] = int(values['annee_construction'])
    values['altitude'] = int(values['altitude'])
    
    # Compute periode class from year
    periode_class = current_app.data.compute_perdiode_class(values['annee_construction'])
    values['periode_construction'] = periode_class
    # Compute altitude class from altitude
    altitude_class = current_app.data.compute_altitude_class(values['altitude'])
    values['classe_altitude'] = altitude_class

    # Inference
    cout, time = current_app.models.predict_cout(values)

    # TODO: process value_1, value_2 and value_3 to get the data
    
    # dummy data
    data = {
        'inference_time_sec': time,
        'result': {
            'prediction': {
                'cout_chauffage_eur': cout
            },
            'inputs': values
        }
    }

    response = jsonify(data)
    response.headers.add("Access-Control-Allow-Origin", "*")

    return response


@api.route('/etiquette_dpe')
def etiquette_dpe():

    values = request.args.to_dict()
    # convert to numeric
    values['annee_construction'] = int(values['annee_construction'])
    values['altitude'] = int(values['altitude'])
    
    # Compute periode class from year
    periode_class = current_app.data.compute_perdiode_class(values['annee_construction'])
    values['periode_construction'] = periode_class
    # Compute altitude class from altitude
    altitude_class = current_app.data.compute_altitude_class(values['altitude'])
    values['classe_altitude'] = altitude_class

    # Inference
    passoire, time = current_app.models.predict_passoire(values)

    # TODO: process value_1, value_2 and value_3 to get the data
    
    # dummy data
    data = {
        'inference_time_sec': time,
        'result': {
            'prediction': {
                'passoire': passoire
            },
            'inputs': values
        }
    }

    response = jsonify(data)
    response.headers.add("Access-Control-Allow-Origin", "*")

    return response