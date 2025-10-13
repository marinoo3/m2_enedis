from flask import Blueprint, render_template, current_app




main = Blueprint('main', __name__)



@main.route('/')
@main.route('/map')
def index():
    data, scales = current_app.data.get_map()
    return render_template('map.html', mapData=data, scales=scales)

@main.route('/statistics')
def statistics():
    df = current_app.data.communes
    test_plot = current_app.plots.test_plot(df)
    return render_template('statistics.html', testPlot=test_plot)

@main.route('/predict')
def predict():
    return render_template('predict.html')