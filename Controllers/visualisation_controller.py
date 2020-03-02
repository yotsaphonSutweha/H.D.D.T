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
            x_axis_value = request.json.get('xValue')
            x_attr_name  = request.json.get('xAttr')
            y_axis_value = request.json.get('yValue')
            y_attr_name = request.json.get('yAttr')
            diagnosis = request.json.get('diagnosis')
            v = Visualisations()
            image = v.generate_scatter_plot(x_attr_name, y_attr_name, int(x_axis_value), int(y_axis_value), int(diagnosis))
            return send_file(image, attachment_filename='plot.png',  mimetype='image/png')


