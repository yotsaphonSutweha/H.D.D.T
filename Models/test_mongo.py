# This module is used as part of unit and functional testing. Making database connection with the testing database.

import os
from flask_mongoengine import MongoEngine
import json
import sys
here = os.path.dirname(os.path.abspath(__file__))
filename = os.path.join(here, './../testenv.json')
with open(filename) as file:
    test_env_details  = json.load(file)
mongo = MongoEngine()
mongo.connect(test_env_details['testEnvInfo']['db-name'], host=test_env_details['testEnvInfo']['db-host'])

