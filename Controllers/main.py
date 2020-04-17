from flask import Blueprint
from .extensions import mongo
from Models.schemas import Doctor
from Models.schemas import Patient
from Models.operations import Operations
import bcrypt
from flask_cors import cross_origin, CORS
from flask import render_template, request, url_for, session, redirect, make_response
from flask_json import as_json, json_response
main = Blueprint('main', __name__)
ops = Operations()
import os 

@main.route('/')
def index():
    # ops.test_add()
    # current_doctor = ops.get_doctor_based_on_doctor_id("yo222")
    # print(current_doctor)
    # print(ops.view_patients_based_on_doctor(current_doctor.id))
    return '<h1>Added a user!</h1>'


@main.route('/logout', methods = ['GET'])
def loggedIn():
    if 'employeeId' in session:
        session.clear()
        url = os.environ.get('ENV_URL') + 'login'
        response = make_response(redirect(url))
        response.set_cookie('hddt', '', max_age=0)
        return response
    error_message = {
        'message': 'You need to login first.'
    }
    return json_response(status_=400, data_ = error_message)

@main.route('/login', methods = ['POST'])
def login():
    if request.method == 'POST':
        employee_id = request.form.get('employeeId') # change to employeeId
        password = request.form.get('password')
        login_doctor = ops.get_doctor_based_on_doctor_id(employee_id)
        login_nurse = ops.get_nurse_based_on_nurse_id(employee_id)
        # do one for nurses as well
        if login_doctor != None and login_nurse == None:
            if bcrypt.hashpw(password.encode('utf-8'), login_doctor['password'].encode('utf-8')) == login_doctor['password'].encode('utf-8'):
                url = os.environ.get('ENV_URL') + 'patients'
                response = make_response(redirect(url))
                response.set_cookie('hddt', 'signed_in_cookie', max_age=60*60)
                session['employeeId'] = employee_id
                return response
            error_message = {
                'message': 'Invalid combinations. Please try again.'
            }
            return json_response(status_=400, data_ = error_message)
        elif login_doctor == None and login_nurse != None:
            if bcrypt.hashpw(password.encode('utf-8'), login_nurse['password'].encode('utf-8')) == login_nurse['password'].encode('utf-8'):
                url = os.environ.get('ENV_URL') + 'patients'
                response = make_response(redirect(url))
                response.set_cookie('hddt', 'signed_in_cookie', max_age=60*60)
                session['employeeId'] = employee_id
                return response
            error_message = {
                'message': 'Invalid combinations. Please try again.'
            }
            return json_response(status_=400, data_ = error_message)
        else:
            error_message = {
                'message': 'Invalid combinations. Please try again.'
            }
            return json_response(status_=400, data_ = error_message)

@main.route('/register', methods = ['POST'])
def register():
    if request.method == 'POST':
        employeeId = request.form.get('employeeId')
        jobRole = request.form.get('jobRole')
        password = request.form.get('password')
        first_name = request.form.get('firstName')
        second_name = request.form.get('secondName')
        contact_number = request.form.get('contactNumber')
        room_number = request.form.get('roomNumber')
        ward = request.form.get('ward')
        checking_doctor = ops.check_if_doctor_exist(employeeId)
        checking_nurse = ops.check_if_nurse_exist(employeeId)
        if checking_doctor == True or checking_nurse == True:
            error_message = {
                'message': 'The employee ID is already exists.'
            }
            return json_response(status_=422, data_ = error_message)
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
                url = os.environ.get('ENV_URL') + 'patients'
                response = make_response(redirect(url))
                response.set_cookie('hddt', 'signed_in_cookie', max_age=60*60)
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
                url = os.environ.get('ENV_URL') + 'patients'
                response = make_response(redirect(url))
                response.set_cookie('hddt', 'signed_in_cookie', max_age=60*60)
                session['employeeId'] = employeeId
                return response
        
