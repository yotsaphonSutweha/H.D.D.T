from flask import Blueprint
from .extensions import mongo
from Models.schemas import Doctor
from Models.schemas import Patient
from Models.operations import Operations
import bcrypt
import json
from flask import render_template, request, url_for, session, redirect, jsonify
from flask_json import as_json, json_response
from flask_cors import cross_origin, CORS
import MachineLearningModels.ml_ops as ml_ops
import os
view_patients_controller = Blueprint('view_patients_controller', __name__)
ops = Operations()

@view_patients_controller.route('/api/view-patients', methods = ['GET'])
@cross_origin(origins='*', methods='GET', supports_credentials='true')
def view_patients():
    if request.method == 'GET':
        if session.get('employeeId') != None:
            employee_id = session['employeeId']
            signed_in_doctor = ops.get_doctor_based_on_doctor_id(employee_id)
            signed_in_nurse = ops.get_nurse_based_on_nurse_id(employee_id)
            if signed_in_doctor != None and signed_in_nurse == None:
                if signed_in_doctor.access_rights["view"] == True:
                    patients = ops.view_patients_based_on_doctor(signed_in_doctor.id)
                    return json_response(status_=200, data_ = patients)
                else: 
                    return '<h1>You do not have access to this functionality</h1>'
            elif signed_in_doctor == None and signed_in_nurse != None:
                if signed_in_nurse.access_rights["viewAll"] == True:
                    # Get every patients within the database
                    return '<h1>Return every patients within the database</h1>'
        else:
            employee_id = session.get('employeeId')
            print(employee_id)
            return '<h1>asas log in</h1>'
    # if request.method == 'GET':
    #     id1 = session.get('employeeId')
    #     print(id1)
    #     response = jsonify({'some': 'data'})
    #     return response
    # return '<h1>No</h1>'

@view_patients_controller.route('/view-patient')
def view_individual_patient():
    if "employeeId" in session:
        patient_id = request.args.get('id')
        employee_id = session['employeeId']
        signed_in_doctor = ops.get_doctor_based_on_doctor_id(employee_id)
        signed_in_nurse = ops.get_nurse_based_on_nurse_id(employee_id)
        if signed_in_nurse == None and signed_in_doctor != None:
            if  signed_in_doctor.access_rights['view'] == True:
                patient = ops.get_patient_based_on_patient_id(patient_id)
                return render_template('patient.html', patient = patient)
            else:
                return '<h1>You do not have access to this functionality</h1>'
        elif signed_in_nurse != None and signed_in_doctor == None:
            if  signed_in_nurse.access_rights['view'] == True:
                patient = ops.get_patient_based_on_patient_id(patient_id)
                return render_template('patient.html', patient = patient)
            else:
                return '<h1>You do not have access to this functionality</h1>'
        else:
            return '<h1>Please log in</h1>'
    else:
        return '<h1>Please log in</h1>'