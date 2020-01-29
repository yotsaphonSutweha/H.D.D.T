from Models.schemas import Doctor, Nurse, Patient
from Controllers.extensions import mongo
import json
class Operations:

    def __ini__(self, name):
        self.name = name

    def check_if_doctor_exist(self, doctor_id):
        check_doctor = False
        try:    
            doctor = self.get_doctor_based_on_doctor_id(doctor_id)
            if doctor != None:
                check_doctor = True
        except:
            check_doctor = False
        return check_doctor

    def check_if_nurse_exist(self, nurse_id):
        check_nurse = False
        try:    
            nurse = self.get_nurse_based_on_nurse_id(nurse_id)
            if nurse != None:
                check_nurse = True
        except:
            check_nurse = False
        return check_nurse

    def register_doctor(self, doctor_id, password, first_name, second_name, contact_number, room_number, ward):
        return Doctor (
            doctor_id=doctor_id,
            password=password,
            first_name=first_name,
            second_name=second_name,
            contact_number=contact_number,
            room_number=room_number,
            ward=ward,
            access_rights = {
                "diagnosis": True,
                "view" : True,
                "modify": True,
                "delete": True,
                "viewAll": False
            }
        ).save()
    
    def register_nurse(self, nurse_id, password, first_name, second_name, contact_number, room_number, ward):
        return Nurse (
            nurse_id=nurse_id,
            password=password,
            first_name=first_name,
            second_name=second_name,
            contact_number=contact_number,
            ward=ward,
            access_rights = {
                "diagnosis": False,
                "view" : True,
                "modify": False,
                "delete": False,
                "viewAll": True
            }
        ).save()


    def view_patients_based_on_doctor(self, doctor_id):
        patients = Patient.objects(assigned_doctor=doctor_id)
        json_data = json.loads(patients.to_json())
        return json_data
    
    def view_every_patients(self):
        patients = Patient.objects()
        json_data = json.loads(patients)
        return json_data

    def get_doctor_based_on_doctor_id(self, doctor_id):
        current_doctor = None
        json_data = None
        try:
            current_doctor = Doctor.objects(doctor_id=doctor_id).get()
            json_data = json.loads(current_doctor.to_json())
        except:
            current_doctor = None
            json_data = current_doctor
        return current_doctor

    def get_nurse_based_on_nurse_id(self, nurse_id):
        current_nurse = None
        json_data = None
        try:
            current_nurse = Nurse.objects(nurse_id=nurse_id).get()
            json_data = json.loads(current_nurse.to_json())
        except:
            current_nurse = None
            json_data = current_nurse
        return current_nurse
    
    def get_patient_based_on_patient_id(self, patient_id):
        patient = Patient.objects(id=patient_id).get()
        json_data = json.loads(patient.to_json())
        return json_data
    

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

        