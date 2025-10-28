from flask import Flask  

from .custom import Data, ENEDIS, ADEME, PlotsManager





def create_app():

    # Create Flask app
    app = Flask(__name__)

    # Load configuration
    print('start')
    with app.app_context():
        app.data = Data()
        app.enedis_api = ENEDIS()
        app.ademe_api = ADEME()
        app.plots = PlotsManager()
    print('done')

    # Init pages routes
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # Init backend ajax 
    from .ajax import ajax as ajax_blueprint
    app.register_blueprint(ajax_blueprint, url_prefix='/ajax')

    # Init API endpoinds
    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')


    return app