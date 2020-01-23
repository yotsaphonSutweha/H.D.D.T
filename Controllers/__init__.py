from flask import Flask
from .extensions import mongo
from .main import main
from .diagnosis_controller import diagnosis_controller
import os
app = Flask(__name__,
            template_folder='../Views/templates',
            static_url_path='',
            static_folder='../Views/static')
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['MONGODB_SETTINGS'] = {
    'db' : 'hddt-database',
    'host' : 'mongodb://oofdon2540:Asd45rty@ds157256.mlab.com:57256/hddt-database?retryWrites=false'
}
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
mongo.init_app(app)
app.register_blueprint(main)
app.register_blueprint(diagnosis_controller)

# @app.after_request
# def add_header(response):
#     response.cache_control.max_age = 0
#     return response

