from flask import Blueprint, send_file
from .extensions import mongo
from Models.schemas import Doctor
from Models.schemas import Patient
from Models.operations import Operations
from flask import render_template, request, url_for, session, redirect
import MachineLearningModels.ml_ops as ml_ops
from Visualisations.visapp import Visualisations
from flask_cors import cross_origin, CORS
from flask_json import as_json, json_response
import json
import matplotlib
from Controllers.controllers_helper import ControllersHelper
helpers = ControllersHelper()
matplotlib.use('agg')
import matplotlib.pyplot as plt
import io

visualisation_controller = Blueprint('visualisation_controller', __name__)
ops = Operations()

@visualisation_controller.route('/api/condition-visualisation', methods=['POST'])
@cross_origin(origins='*', methods='POST', supports_credentials='true')
def condition_visualisation():
    if request.method == 'POST':
        if  'employeeId' in session:
            logged_in_user_id = session['employeeId']
            doctor = ops.get_doctor_based_on_doctor_id(logged_in_user_id)
            nurse = ops.get_nurse_based_on_nurse_id(logged_in_user_id)
            if doctor != None and nurse == None and doctor.access_rights['diagnosis'] == True:
                x_axis_value = request.json.get('xValue')
                x_attr_name  = request.json.get('xAttr')
                y_axis_value = request.json.get('yValue')
                y_attr_name = request.json.get('yAttr')
                diagnosis = request.json.get('diagnosis')
                if helpers.check_x_and_y_axis_name(x_attr_name, y_attr_name, x_axis_value, y_axis_value):
                    error_message = {
                        'message': 'Please choose appropriate medical data option in the drop down(s).'
                    }
                    return json_response(status_= 400, data_ = error_message)
                else:
                    v = Visualisations()
                    image = v.generate_scatter_plot(x_attr_name, y_attr_name, int(x_axis_value), int(y_axis_value), int(diagnosis))
                    return send_file(image, attachment_filename='plot.png',  mimetype='image/png')
            elif doctor == None and nurse != None and nurse.access_rights['diagnosis'] == False:
                error_message = {
                    'message': 'You do not have access to this functionality.'
                }
                return json_response(status_= 403, data_ = error_message)
        else: 
            error_message = {
                'message' : 'Please log in.'
            }
            return json_response(status_=400, data_ = error_message)
   

