from flask import Blueprint
from .extensions import mongo
from Models.schemas import Doctor
from Models.schemas import Patient
from Models.operations import Operations
import bcrypt
import json
from flask import render_template, request, url_for, session, redirect, jsonify, make_response
from flask_json import as_json, json_response
from flask_cors import cross_origin, CORS
import MachineLearningModels.ml_ops as ml_ops
import os
patients_controller = Blueprint('patients_controller', __name__)
ops = Operations()

@patients_controller.route('/api/patients', methods = ['GET'])
@cross_origin(origins='*', methods='GET', supports_credentials='true')
def view_patients():
    if request.method == 'GET':
        if session.get('employeeId') != None:
            employee_id = session['employeeId']
            signed_in_doctor = ops.get_doctor_based_on_doctor_id(employee_id)
            signed_in_nurse = ops.get_nurse_based_on_nurse_id(employee_id)
            if request.args.get('q') == 'waiting-list':
                data = ops.get_patients_with_severity()
                return json_response(data_ = data)
            else: 
                if signed_in_doctor != None and signed_in_nurse == None:
                    if signed_in_doctor.access_rights["view"] == True:
                        patients = ops.get_patients_based_on_doctor(signed_in_doctor.id)
                        return json_response(data_ = patients)
                    else: 
                        error_message = {
                            'message': 'You do not have access to this functionality'
                        }
                        return json_response(status_=403, data_ = error_message)
                elif signed_in_doctor == None and signed_in_nurse != None:
                    if signed_in_nurse.access_rights["viewAll"] == True:
                        patients = ops.get_every_patients()
                        return json_response(data_ = patients)
                    else: 
                        error_message = {
                            'message': 'You do not have access to this functionality'
                        }
                        return json_response(status_=403, data_ = error_message)
        else:
            error_message = {
                'message' : 'Please log in'
            }
            return json_response(status_=401, data_ = error_message)
   

@patients_controller.route('/api/patient', methods = ['GET', 'POST', 'DELETE'])
@cross_origin(origins="*", methods=['GET', 'POST', 'DELETE'], supports_credentials='true')
def view_individual_patient():
    if "employeeId" in session:
        employee_id = session['employeeId']
        patient_id = request.args.get('id')
        if request.method == 'GET':
            signed_in_doctor = ops.get_doctor_based_on_doctor_id(employee_id)
            signed_in_nurse = ops.get_nurse_based_on_nurse_id(employee_id)
            if signed_in_nurse == None and signed_in_doctor != None:
                if  signed_in_doctor.access_rights['view'] == True:
                    patient = ops.get_patient_based_on_patient_id(patient_id)
                    return json_response(status_=200, data_ = patient)
                else:
                    error_message = {
                        'message': 'You do not have access to this functionality'
                    }
                    return json_response(status_=403, data_ = error_message)

            elif signed_in_nurse != None and signed_in_doctor == None:
                if  signed_in_nurse.access_rights['view'] == True:
                    patient = ops.get_patient_based_on_patient_id(patient_id)
                    return json_response(status_=200, data_ = patient)
                else:
                    error_message = {
                        'message': 'You do not have access to this functionality'
                    }
                    return json_response(status_=403, data_ = error_message)
            else:
                error_message = {
                    'message' : 'Please log in'
                }
                return json_response(status_=401, data_ = error_message)

        elif request.method == 'POST':
            query = request.args.get('q')
            if query == 'update':
                new_patient_details = request.json
                ops.update_patient_details(patient_id, new_patient_details['first_name'], new_patient_details['second_name'], new_patient_details['address'], new_patient_details['contact_number'], new_patient_details['next_of_kin1_first_name'], new_patient_details['next_of_kin1_second_name'], new_patient_details['next_of_kin2_first_name'], new_patient_details['next_of_kin2_second_name']) # add the severity
                successful_message = {
                    'message' : 'Details updated successfully'
                }
                return json_response(status_ = 200, data_= successful_message)
            else:
                error_message = {
                    'message' : 'Operation not supported'
                }
                return json_response(data_ = error_message)

        elif request.method == 'DELETE':
            query = request.args.get('q')
            if query == 'delete':
                patient = request.json
                ops.delete_patient(patient['patient_id'])
                successful_message = {
                    'message' : 'Selected patient has been deleted'
                }
                return json_response(status_ = 200, data_= successful_message)
            else:
                error_message = {
                    'message' : 'Operation not supported'
                }
                return json_response(data_ = error_message)

    else:
        error_message = {
            'message' : 'Please log in'
        }
        return json_response(status_=401, data_ = error_message)

@patients_controller.route('/api/assign-severity', methods = ['POST'])
@cross_origin(origins="*", methods=['POST'], supports_credentials='true')
def assign_severity():
    if 'employeeId' in session:
        employee_id = session['employeeId']
        patient_id = request.json.get('patientId')
        if request.method == 'POST':
            signed_in_doctor = ops.get_doctor_based_on_doctor_id(employee_id)
            signed_in_nurse = ops.get_nurse_based_on_nurse_id(employee_id)
            if signed_in_nurse == None and signed_in_doctor != None:
                if  signed_in_doctor.access_rights['diagnosis'] == True:
                    patient_severity = request.json.get('severity')
                    ops.assign_severity(patient_id, patient_severity)
                    success_message = {
                        'message': 'The patient has been with severity'
                    }
                    return json_response(status_= 200, data_ = success_message)
                else:
                    error_message = {
                        'message': 'You do not have access to this functionality'
                    }
                    return json_response(status_=403, data_ = error_message)
            else:
                error_message = {
                    'message': 'You do not have access to this functionality'
                }
                return json_response(status_=403, data_ = error_message)
        return True
    else:
        error_message = {
            'message' : 'Please log in'
        }
        return json_response(status_=401, data_ = error_message)