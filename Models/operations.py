from Models.schemas import Doctor
from Models.schemas import Patient
from Controllers.extensions import mongo
import json
class Operations:

    def __ini__(self, name):
        self.name = name

    def view_patients_based_on_doctor(self, doctor_id):
        patients = Patient.objects(assigned_doctor=doctor_id)
        json_data = patients.to_json()
        return json_data

    def get_doctor_based_on_doctor_id(self, doctor_id):
        current_doctor = Doctor.objects(doctor_id=doctor_id).get()
        return current_doctor

    def add_patient(self, current_doctor, first_name, second_name, address, contact_number, next_of_kin1_first_name, next_of_kin1_second_name, next_of_kin2_first_name, next_of_kin2_second_name, severity, medical_data):

        return Patient (
            assigned_doctor = current_doctor,
            first_name = first_name,
            second_name = second_name,
            address = address,
            contact_number = contact_number,
            next_of_kin1_first_name = next_of_kin1_first_name,
            next_of_kin1_second_name = next_of_kin1_second_name,
            next_of_kin2_first_name = next_of_kin2_first_name,
            next_of_kin2_second_name = next_of_kin2_second_name,
            severity = severity,
            medical_data = medical_data
        ).save()


    def test_add(self):
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
            first_name = "yooooooo",
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

        