from flask import Blueprint
from .extensions import mongo
from Models.schemas import Doctor
from Models.schemas import Patient
from Models.operations import Operations
main = Blueprint('main', __name__)
ops = Operations()
    
@main.route('/')
def index():
    ops.test_add()
    # id1 = 0
    # current_doctor = ops.get_doctor_based_on_doctor_id("yo222")
    # print(current_doctor)
    # print(ops.view_patients_based_on_doctor(current_doctor.id))
    return '<h1>Added a user!</h1>'