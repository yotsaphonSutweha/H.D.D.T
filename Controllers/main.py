from flask import Blueprint
from .extensions import mongo
from Models.schemas import Doctor
from Models.schemas import Patient
from Models.operations import Operations
from flask import render_template, request, url_for
main = Blueprint('main', __name__, template_folder='../Views/templates')
ops = Operations()
    
@main.route('/')
def index():
    # ops.test_add()
    # current_doctor = ops.get_doctor_based_on_doctor_id("yo222")
    # print(current_doctor)
    # print(ops.view_patients_based_on_doctor(current_doctor.id))
    return '<h1>Added a user!</h1>'

@main.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        doctor_id = request.form.get('doctorId')
        password = request.form.get('password')
        first_name = request.form.get('firstName')
        second_name = request.form.get('secondName')
        contact_number = request.form.get('contactNumber')
        room_number = request.form.get('roomNumber')
        ward = request.form.get('ward')

        ops.register_doctor (
            doctor_id,
            password,
            first_name,
            second_name,
            contact_number, 
            room_number,
            ward
        )
        return render_template("message-prompt.html")


    return render_template("registration.html")
        
