from flask import Flask  

from .custom import Data, ENEDIS, ADEME





def create_app():

    # Create Flask app
    app = Flask(__name__)

    # Load configuration
    with app.app_context():
        app.data = Data()
        app.enedis_api = ENEDIS()
        app.ademe_api = ADEME()

    # Init pages routes (only tye map for now)
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # Init endpoints 
    from .endpoints import endpoints as endpoints_blueprint
    app.register_blueprint(endpoints_blueprint, url_prefix='/api')


    return app