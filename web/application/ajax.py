from flask import Blueprint, Response, request, jsonify, stream_with_context, current_app
import json
from datetime import datetime



ajax = Blueprint('ajax', __name__)



@ajax.route('/update_data/', methods=['GET'])
def update_data() -> Response:

    """Call Enedis API to update the data and save it on the Koyeb volume

    Returns:
        Response: A streaming response with MIME type 'text/event-stream' to facilitate stream

    Yields:
        str: Stream progress in the form of "data:{progress}\n\n" where `progress`
        is the percentage of completion of the API call
    """

    print('DEBUG: init data update')

    def collect():

        # last_update = current_app.data.get_property('update')
        # date = datetime.strptime(last_update, '%d-%m-%Y')

        enedis_data = yield from current_app.enedis_api.communes(yield_progress=True)
        current_app.data.update_communes(enedis_data)

        # TODO: Update the logements data, format it with the pipeline and save it to volume
        # ademe_data = yield from current_app.ademe_api.addresses_from_date(date, yield_progress=True)
        # current_app.data.update_logements(ademe_data['existing'], ademe_data['new'])

        yield 'data:complete\n\n'

    return Response(
        stream_with_context(collect()),
        mimetype = "text/event-stream",
        headers={
            'Cache-Control': 'no-cache',
            'X-Accel-Buffering': 'no'  # for nginx buffering
        }
    )

@ajax.route('/update_data1/', methods=['GET'])
def update_data1() -> Response:

    """Call Enedis API to update the data and save it on the Koyeb volume

    Returns:
        Response: A streaming response with MIME type 'text/event-stream' to facilitate stream

    Yields:
        str: Stream progress in the form of "data:{progress}\n\n" where `progress`
        is the percentage of completion of the API call
    """

    print('DEBUG: init data update')

    def collect():

        last_update = current_app.data.get_property('update')
        date = datetime.strptime(last_update, '%d-%m-%Y')

        enedis_data = yield from current_app.enedis_api.communes(yield_progress=True)
        current_app.data.update_communes(enedis_data)

        # ademe_existing = current_app.ademe_api.addresses_from_date(date, yield_progress=True)
        # print(len(ademe_existing))
        #current_app.data.update_logements(ademe_existing, ademe_new)
        ## TODO: clean the data here through a pipe line then append to the existing one and save it on the volume


    collect()

    return jsonify('complete')


@ajax.route('/map_data/', methods=['GET'])
def map_data() -> Response:

    """Filters map data, don't works for zoomed map data yet

    Args:
        filters {json} -- List of filter rules (default None)
        sort {json} -- How to sort the data (default None)

    Returns:
        Response: Filtered data
    """

    # Retrieve request parameters
    filters = request.args.get('filters')
    if filters: 
        filters = json.loads(filters)

    sort = request.args.get('sort')
    if sort: 
        sort = json.loads(sort)

    # Filters data
    data, scales = current_app.data.get_map(filters=filters, sort=sort)
    return jsonify({
        'data': data, 
        'scales': scales
    })


@ajax.route('/zoomed_map_data/', methods=['GET'])
def zoomed_map_data() -> Response:

    """Collect a list of streets from a specific bounding box with Ademe API 
    and collect the corresponfing streets data with Enedis API.

    Args:
        minLongitude {float} -- bbox minimum longitude
        minLatitude {float} -- bbox minimum latitude
        maxLongitude {float} -- bbox maximum longitude
        maxLatitude {float} -- bbox maximum latitude

    Returns:
        Response: Map data from a specific bounding box

    Yields:
        json: Map data chunk
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

            batch_iris, offset = current_app.enedis_api.iris_from_insee(insee_codes, offset=offset)
            data = current_app.data.get_zoomed_map(streets, batch_iris) # concate and format data

            if data == []: 
                continue # skip if no data

            # Extend data
            iris_data.extend(data)
            yield json.dumps(iris_data) + '\n'

    return Response(
        stream_with_context(collect()),
        content_type = "application/json",
        headers = {
            'Cache-Control': 'no-cache',
            'X-Accel-Buffering': 'no'  # helps bypass nginx buffering
        }
    )
