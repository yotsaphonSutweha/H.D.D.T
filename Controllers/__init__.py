from flask import Flask
from .extensions import mongo
from .main import main

def create_app():
    app = Flask(__name__)

    app.config['MONGODB_SETTINGS'] = {
        'db' : 'hddt-database',
        'host' : 'mongodb://oofdon2540:Asd45rty@ds157256.mlab.com:57256/hddt-database?retryWrites=false'
    }
    
    mongo.init_app(app)
    app.register_blueprint(main)

    return app