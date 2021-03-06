from flask import Blueprint
from .extensions import mongo
from Models.schemas import Doctor
from Models.schemas import Patient
from Models.operations import Operations
import bcrypt
from flask_cors import cross_origin, CORS
from flask import render_template, request, url_for, session, redirect, make_response
from flask_json import as_json, json_response
import re
main = Blueprint('main', __name__)
ops = Operations()
import os 


@main.route('/')
def index():
    message = {
        'message': 'HDDT backend server started.'
    }
    return json_response(status_= 200, data_ = message)


# The logout endpoint implementation:
# Step 1: check for the user session 
# Step 2: clear the session 
# If there is no session, returns the error message

@main.route('/api/logout', methods = ['GET'])
@cross_origin(origins='*', methods='GET', supports_credentials='true')
def logout():
    if 'employeeId' in session:
        session.clear()
        response = make_response()
        return response
    error_message = {
        'message': 'You need to log in first.'
    }
    return json_response(status_=400, data_ = error_message)

# The login endpoint implementation:
# Step 1: check if the request is post
# Step 2: query the database to check if the provided employee details exist
# Step 3: if the employee id exists as doctor or nurse, log the user in and create the session. Otherwise returns error message back to the user.

@main.route('/api/login', methods = ['POST'])
@cross_origin(origins='*', methods='POST', supports_credentials='true')
def login():
    if request.method == 'POST':
        employee_id = request.json.get('employee_id') 
        password = request.json.get('password')
        login_doctor = ops.get_doctor_based_on_doctor_id(employee_id)
        login_nurse = ops.get_nurse_based_on_nurse_id(employee_id)
        if login_doctor != None and login_nurse == None:
            if bcrypt.hashpw(password.encode('utf-8'), login_doctor['password'].encode('utf-8')) == login_doctor['password'].encode('utf-8'):
                response = make_response()
                session['employeeId'] = employee_id
                return response
            error_message = {
                'message': 'Invalid combinations. Please try again.'
            }
            return json_response(status_=400, data_ = error_message)
        elif login_doctor == None and login_nurse != None:
            if bcrypt.hashpw(password.encode('utf-8'), login_nurse['password'].encode('utf-8')) == login_nurse['password'].encode('utf-8'):
                response = make_response()
                session['employeeId'] = employee_id
                return response
            error_message = {
                'message': 'Invalid combinations. Please try again.'
            }
            return json_response(status_=400, data_ = error_message)
        else:
            error_message = {
                'message': 'No account exists with the given employee ID. Please register a new user account.'
            }
            return json_response(status_=400, data_ = error_message)


# The registration endpoint implementation:
# Step 1: check if the request is POST
# Step 2: get user's information from the request
# Step 3: validates the user's inputs such as checking if the employee id is already exists, and checking the format of the information is correct.
# Step 4: if everything pass the validations, the user's information will be inserted into the database. If not, provide the users with appropriate error message.

@main.route('/api/register', methods = ['POST'])
@cross_origin(origins='*', methods='POST', supports_credentials='true')
def register():
    if request.method == 'POST':
        employeeId = request.json.get('employee_id')
        jobRole = request.json.get('job_role')
        password = request.json.get('password')
        confirm_password = request.json.get('confirm_password')
        first_name = request.json.get('first_name')
        second_name = request.json.get('second_name')
        contact_number = request.json.get('contact_number')
        room_number = request.json.get('room')
        ward = request.json.get('ward')
        checking_doctor = ops.check_if_doctor_exist(employeeId)
        checking_nurse = ops.check_if_nurse_exist(employeeId)
        print('password length {0}'.format(len(password)))
        if checking_doctor == True or checking_nurse == True:
            error_message = {
                'message': 'The employee ID already exists.'
            }
            return json_response(status_=400, data_ = error_message)
        else:
            if password != confirm_password:
                error_message = {
                    'message': 'Password and comfirm password are not the same.'
                }
                return json_response(status_=400, data_ = error_message)
            else:
                if len(password) < 8 or not password.isalnum():
                    error_message = {
                        'message': 'Password must contain the minimum of 8 characters with the combination of letters or numbers.'
                    }
                    return json_response(status_=400, data_ = error_message)
                else:
                    if not contact_number.isdigit() or len(contact_number) > 10:
                        error_message = {
                            'message': 'The contact number must contain only digits and follow the Irish phone number standard ie. 08xxxxxxxx.'
                            }
                        return json_response(status_=400, data_ = error_message)
                    else:
                        if len(room_number) > 3:
                            error_message = {
                                'message': 'Room number must be less than 3 characters.'
                            }
                            return json_response(status_=400, data_ = error_message)
                        else:
                            if len(ward) > 10:
                                error_message = {
                                    'message': 'Please provide an appropriate  ward location.'
                                }
                                return json_response(status_=400, data_ =   error_message)
                            else:
                                if len(first_name) > 40 or len(second_name) > 40:
                                    error_message = {
                                        'message': 'The minimum length of first and second name characters must not exceed 40 letters.'
                                    }
                                    return json_response(status_=400, data_ =   error_message)
                                else:
                                    if len(employeeId) > 8 or not employeeId.isalnum():
                                        error_message = {
                                            'message': 'The Employee ID must be less than 8 characters with the combination of letters or numbers.'
                                        }
                                        return json_response(status_=400, data_ = error_message)
                                    else:
                                        if jobRole == 'Doctor': 
                                            hased_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                                            ops.register_doctor (
                                                employeeId,
                                                hased_password,
                                                first_name,
                                                second_name,
                                                contact_number, 
                                                room_number,
                                                ward
                                            )
                                            response = make_response()
                                            session['employeeId'] = employeeId
                                            return response
                                        elif jobRole == 'Nurse':
                                            hased_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                                            ops.register_nurse (
                                                employeeId,
                                                hased_password,
                                                first_name,
                                                second_name,
                                                contact_number, 
                                                room_number,
                                                ward
                                            )
                                            response = make_response()
                                            session['employeeId'] = employeeId
                                            return response
                                        else:
                                            error_message = {
                                                'message': 'Please provide an appropriate job role.'
                                            }
                                            return json_response(status_=400, data_ =error_message)
                                    
