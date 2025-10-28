from flask import Blueprint, render_template, current_app



main = Blueprint('main', __name__)



@main.context_processor
def inject_update_date():

    """Retrieve last update date from volume properties and pass it to each route as `update_date`

    Returns:
        dict: `update_date` data for the HTML header
    """

    date = current_app.data.get_property('update')
    return {'update_date': date}



@main.route('/')
@main.route('/map')
def index():
    data, scales = current_app.data.get_map()
    return render_template('map.html', current_page="map", mapData=data, scales=scales)

@main.route('/statistics')
def statistics():
    df = current_app.data.get_plot()
    plot_jsons = current_app.plots.get_jsons(df=df)
    return render_template('statistics.html', current_page="statistics", **plot_jsons)

@main.route('/predict')
def predict():
    return render_template('predict.html', current_page="predict")

@main.route('/api-documentation')
def api_documentation():
    return render_template('api-documentation.html', current_page="api-documentation")