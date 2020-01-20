from flask import Blueprint
from .extensions import mongo
from Models.schemas import Doctor
from Models.schemas import Patient
main = Blueprint('main', __name__)

    
@main.route('/')
def index():
    doctor1 = Doctor (
        doctor_id="yo111",
        password="asd",
        first_name="yotsaphon",
        second_name="sutweha",
        contact_number="0868441277",
        room_number="d1",
        ward="north1",
        access_rights = {
            "view" : True
        }
    ).save()

    patient1 = Patient (
        assigned_doctor = doctor1,
        first_name = "aaa",
        second_name = "bbb",
        address = "53 Abbey street Dublin 1",
        contact_number = "8776544",
        next_of_kin1_first_name = "gggg",
        next_of_kin1_second_name = "bbb",
        next_of_kin2_first_name = "ddd",
        next_of_kin2_second_name = "aaa",
        severity = 1,
        medical_data = {
            "diagnosed" : False 
        }
    ).save()
    return '<h1>Added a user!</h1>'