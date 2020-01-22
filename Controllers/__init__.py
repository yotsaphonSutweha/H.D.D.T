from flask import Flask
from .extensions import mongo
from .main import main

app = Flask(__name__,
            template_folder='../Views/templates')

app.config['MONGODB_SETTINGS'] = {
    'db' : 'hddt-database',
    'host' : 'mongodb://oofdon2540:Asd45rty@ds157256.mlab.com:57256/hddt-database?retryWrites=false'
}
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
mongo.init_app(app)
app.register_blueprint(main)

