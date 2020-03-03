from flask import Blueprint
from .extensions import mongo
from Models.schemas import Doctor
from Models.schemas import Patient
from Models.operations import Operations
import bcrypt
from flask_cors import cross_origin, CORS
from flask import render_template, request, url_for, session, redirect, make_response
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
        url = os.environ.get('ENV_URL')
        response = make_response(redirect(url))
        return response
    return '<h1>You need to log in</h1>'

@main.route('/login', methods = ['POST'])
def login():
    if request.method == 'POST':
        doctor_id = request.form.get('doctorId')
        password = request.form.get('password')
        login_doctor = ops.get_doctor_based_on_doctor_id(doctor_id)
        # do one for nurses as well
        if login_doctor != None:
            if bcrypt.hashpw(password.encode('utf-8'), login_doctor['password'].encode('utf-8')) == login_doctor['password'].encode('utf-8'):
                resp = make_response(redirect('/'))
                session['employeeId'] = doctor_id
                url = os.environ.get('ENV_URL') + 'patients'
                response = make_response(redirect(url))
                return response
            return '<h1>Invalid combination</h1>'
        else:
            return '<h1>Please sign up</h1>'

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
            return '<h1>Use is already existed</h1>' 
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
                session['employeeId'] = employeeId
                url = os.environ.get('ENV_URL') + 'patients'
                return redirect(url)

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
                session['employeeId'] = employeeId
                url = os.environ.get('ENV_URL') + 'patients'
                return redirect(url_for(url))
        
