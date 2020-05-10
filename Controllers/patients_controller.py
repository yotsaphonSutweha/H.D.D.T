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
from Controllers.controllers_helper import ControllersHelper
patients_controller = Blueprint('patients_controller', __name__)
ops = Operations()
helpers = ControllersHelper()


# The view patients endpoint implementation:
# Step 1: check if the request is get
# Step 2: check if the user session exists
# Step 3: check the user's access to the funtionality and the user's query to provide appropriate response 
# Step 4: if every pass, the endpoint should return the list of patients as the response. Otherwise, the error message will be sent instead.

@patients_controller.route('/api/patients', methods = ['GET'])
@cross_origin(origins='*', methods='GET', supports_credentials='true')
def view_patients():
    if request.method == 'GET':
        if session.get('employeeId') != None:
            employee_id = session['employeeId']
            signed_in_doctor = ops.get_doctor_based_on_doctor_id(employee_id)
            signed_in_nurse = ops.get_nurse_based_on_nurse_id(employee_id)
            if (signed_in_doctor != None and signed_in_nurse == None) and (signed_in_doctor.access_rights['view'] and request.args.get('q') == 'waiting-list'):
                data = ops.get_patients_with_severity(signed_in_doctor.id)
                return json_response(data_ = data)
            elif (signed_in_doctor == None and signed_in_nurse != None) and (signed_in_nurse.access_rights['viewAll'] and request.args.get('q') == 'waiting-list'):
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
                'message' : 'Please log in.'
            }
            return json_response(status_=400, data_ = error_message)
   
# This endpoint accepts multiple HTTP methods including get, post, and delete. The GET request is for viewing an information of a patient, POST is for modifying, DELETE is for deleting the patient.

# Implementation for GET
# Step 1: check if the user session exists
# Step 2: check if the request is get
# Step 3: check the user's access to the funtionality to provide appropriate response 
# Step 4: if every pass, the endpoint should return the patient's information as the response. Otherwise, the error message will be sent instead.

# Implementation for POST
# Step 1: check if the user session exists
# Step 2: check if the request is POST
# Step 3: check the user's access to the funtionality and the query to provide appropriate response 
# Step 4: get the new information of the patient from the request to make an update
# Step 5: if every pass, the endpoint should modify the patient's information. Otherwise, the error message will be sent instead.

# Implementation for Delete
# Step 1: check if the user session exists
# Step 2: check if the request is DELETE
# Step 3: check the user's access to the funtionality and the query to provide appropriate response 
# Step 4: get the patient id and use it to delete the patient from the database.
# Step 5: if every pass, the endpoint should delete the patient. Otherwise, the error message will be sent instead.

@patients_controller.route('/api/patient', methods = ['GET', 'POST', 'DELETE'])
@cross_origin(origins="*", methods=['GET', 'POST', 'DELETE'], supports_credentials='true')
def view_individual_patient():
    if "employeeId" in session:
        employee_id = session['employeeId']
        patient_id = request.args.get('id')
        signed_in_doctor = ops.get_doctor_based_on_doctor_id(employee_id)
        signed_in_nurse = ops.get_nurse_based_on_nurse_id(employee_id)
        if request.method == 'GET':
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
        elif request.method == 'POST':
            query = request.args.get('q')
            if query == 'update':
                if (signed_in_doctor != None and signed_in_nurse == None and signed_in_doctor.access_rights['modify'] == True) or (signed_in_doctor == None and signed_in_nurse != None and signed_in_nurse.access_rights['modify'] == True):
                    # Impplement checking here
                    new_patient_details = request.json
                    first_name = new_patient_details['first_name']
                    second_name = new_patient_details['second_name']
                    address = new_patient_details['address']
                    contact_number = new_patient_details['contact_number']
                    next_of_kin1_first_name = new_patient_details['next_of_kin1_first_name']
                    next_of_kin1_second_name = new_patient_details['next_of_kin1_second_name']
                    next_of_kin2_first_name = new_patient_details['next_of_kin2_first_name']
                    next_of_kin2_second_name =  new_patient_details['next_of_kin2_second_name']
                    if helpers.check_information_length(first_name, second_name, address, contact_number, next_of_kin1_first_name, next_of_kin1_second_name, next_of_kin2_first_name, next_of_kin2_second_name):
                        ops.update_patient_details(patient_id, first_name, second_name, address, contact_number, next_of_kin1_first_name, next_of_kin1_second_name, next_of_kin2_first_name, next_of_kin2_second_name) # add the severity
                        successful_message = {
                            'message' : 'Details updated successfully.'
                        }
                        return json_response(status_ = 200, data_= successful_message)
                    else:
                        error_message = {
                            'message': 'Please provide an appropriate information.'
                        }
                        return json_response(status_= 400, data_ = error_message)
                else:
                    error_message = {
                        'message': 'You do not have access to this functionality.'
                    }
                    return json_response(status_=403, data_ = error_message)
            else:
                error_message = {
                    'message' : 'Operation not supported.'
                }
                return json_response(status_= 404, data_ = error_message)
        elif request.method == 'DELETE':
            query = request.args.get('q')
            if query == 'delete':
                # Impplement checking here
                if (signed_in_doctor != None and signed_in_nurse == None and signed_in_doctor.access_rights['delete'] == True) or (signed_in_doctor == None and signed_in_nurse != None and signed_in_nurse.access_rights['delete'] == True):
                    patient = request.json
                    ops.delete_patient(patient['patient_id'])
                    successful_message = {
                        'message' : 'Selected patient has been deleted.'
                    }
                    return json_response(status_ = 200, data_= successful_message)
                else:
                    error_message = {
                        'message': 'You do not have access to this functionality'
                    }
                    return json_response(status_=403, data_ = error_message)
            else:
                error_message = {
                    'message' : 'Operation not supported.'
                }
                return json_response(status_= 404, data_ = error_message)
    else:
        error_message = {
            'message' : 'Please log in.'
        }
        return json_response(status_=400, data_ = error_message)

# The assign severity endpoint implementation:
# Step 1: check if the user session exists
# Step 2: check if the request is POST
# Step 3: check the user's access to the funtionality 
# Step 4: validates the user's request
# Step 4: if everything pass, the endpoint should assign the severity to the patient. Otherwise, the error message will be sent instead.

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
                    try:
                        if int(patient_severity) > 5 or int(patient_severity) < 0:
                            error_message = {
                                'message': 'The severity level ranging from 0 to 5. Please assign an appropriate severity level.'
                            }
                            return json_response(status_=400, data_ = error_message)
                        else:
                            ops.assign_severity(patient_id, patient_severity)
                            success_message = {
                                'message': 'The patient has been assigned with severity.'
                            }
                            return json_response(status_= 200, data_ = success_message)
                    except:
                        error_message = {
                                'message': 'Please provide severity as numbers. The severity level ranging from 0 to 5.'
                            }
                        return json_response(status_=400, data_ = error_message)
                else:
                    error_message = {
                        'message': 'You do not have access to this functionality.'
                    }
                    return json_response(status_=403, data_ = error_message)
            else:
                error_message = {
                    'message': 'You do not have access to this functionality.'
                }
                return json_response(status_=403, data_ = error_message)
        return True
    else:
        error_message = {
            'message' : 'Please log in.'
        }
        return json_response(status_=400, data_ = error_message)
