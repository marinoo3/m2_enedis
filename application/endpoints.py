from flask import Blueprint, Response, request, jsonify, stream_with_context, current_app
import json




endpoints = Blueprint('api', __name__)




@endpoints.route('/simple_query/<query>', methods=['GET'])
def simple_query(query:str):

    """
    Simple query exemple
    """

    print(query)
    return


@endpoints.route('/map_data/', methods=['GET'])
def map_data():

    """
    Filters map data, don't works for zoomed map data yet
    * `year` and `state` passed as argument
    Returns the filtered data
    """

    # Retrieve request parameters
    code_commune = request.args.get('code_commune')
    annee = request.args.get('annee')

    # Build filters
    filters = {}
    if code_commune: filters['code_commune'] = code_commune
    if annee: filters['annee'] = annee

    # Filters data
    data = current_app.data.get_map(filters)
    return jsonify(data)


@endpoints.route('/zoomed_map_data/', methods=['GET'])
def zoomed_map_data():

    """
    Requests precise data for the map giving a specific bounding box
    * Bounding box passed as 4 arguments: `minLongitude`, `minLatitude`, `maxLongitude`, `maxLatitude`
    Returns iris data formatted for the map
    """

    # Retrieve request parameters
    min_lon = request.args.get('minLongitude')
    min_lat = request.args.get('minLatitude')
    max_lon = request.args.get('maxLongitude')
    max_lat = request.args.get('maxLatitude')

    # Get streets data from ademe API
    streets:list[dict] = current_app.ademe_api.insee_from_bbox(min_lon, min_lat, max_lon, max_lat)
    # Collect insee codes from streets data
    insee_codes = [ row['code_insee_ban'] for row in streets ]
    insee_codes = list(set(insee_codes)) # remove duplicates

    # Get iris data from enedis API
    iris_data = []
    def collect():
        offset = 0
        while offset is not None:
            # Get iris
            batch_iris, offset = current_app.enedis_api.iris_from_insee(insee_codes, offset=offset)
            # Concate and format data
            data = current_app.data.get_zoomed_map(streets, batch_iris)
            if data == []: 
                continue # skip if no data
            # Extend data
            iris_data.extend(data)
            yield json.dumps(iris_data) + '\n'

    return Response(
        stream_with_context(collect()),
        content_type = "application/json",
        # headers = {
        #     'Cache-Control': 'no-cache',
        #     'X-Accel-Buffering': 'no'  # helps bypass Nginx buffering
        # }
    )

