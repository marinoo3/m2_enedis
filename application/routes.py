from flask import Blueprint, render_template, current_app



main = Blueprint('main', __name__)



@main.route('/')
def index():
    data = current_app.data.get_map_data()
    return render_template('map.html', mapData=data)