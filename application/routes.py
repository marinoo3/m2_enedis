from flask import Blueprint, render_template, current_app



main = Blueprint('main', __name__)



@main.route('/')
@main.route('/map')
def index():
    data = current_app.data.get_map()
    return render_template('map.html', mapData=data)

@main.route('/statistics')
def statistics():
    return render_template('statistics.html')

@main.route('/predict')
def predict():
    return render_template('predict.html')