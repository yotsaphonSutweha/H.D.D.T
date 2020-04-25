# Comment Controllers.extensions import mongo to run unit tests
from Controllers.extensions import mongo 
import json

# Uncomment below to run unit tests
# import sys
# sys.path.insert(1, './../../')
# ------End of uncomment-------
from Models.schemas import Doctor, Nurse, Patient
class Operations:
    def __init__(self):
        super().__init__()

    # done
    def check_if_doctor_exist(self, doctor_id):
        check_doctor = False
        try:    
            doctor = self.get_doctor_based_on_doctor_id(doctor_id)
            if doctor != None:
                check_doctor = True
        except:
            check_doctor = False
        return check_doctor

    # done
    def check_if_nurse_exist(self, nurse_id):
        check_nurse = False
        try:    
            nurse = self.get_nurse_based_on_nurse_id(nurse_id)
            if nurse != None:
                check_nurse = True
        except:
            check_nurse = False
        return check_nurse

    # done
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
    
    # done
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
                "modify": True,
                "delete": True,
                "viewAll": True
            }
        ).save()

    # done
    def get_patients_based_on_doctor(self, doctor_id):
        patients = Patient.objects(assigned_doctor=doctor_id)
        json_data = json.loads(patients.to_json())
        return json_data
    
    # done
    def get_every_patients(self):
        patients = Patient.objects()
        json_data = json.loads(patients.to_json())
        return json_data

    # done
    def get_patients_with_severity(self, doctor_id=None):
        json_data = {}
        if doctor_id != None:
            patients_with_severity = Patient.objects(assigned_doctor=doctor_id, severity__gt=0).order_by('-severity')
            json_data = json.loads(patients_with_severity.to_json())
            return json_data
        else:
            patients_with_severity = Patient.objects(severity__gt=0).order_by('-severity')
            json_data = json.loads(patients_with_severity.to_json())
            return json_data

    # done
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

    # not in use
    def get_every_doctors(self):
        doctors = None 
        json_data = None 
        try:
            doctors = Doctor.objects().get()
            json_data = json.loads(doctors)
        except:
            doctors = None
            json_data = doctors
        return json_data

    # done
    def get_nurse_based_on_nurse_id(self, nurse_id):
        current_nurse = None
        try:
            current_nurse = Nurse.objects(nurse_id=nurse_id).get()
        except:
            current_nurse = None
        return current_nurse
    
    # done
    def get_patient_based_on_patient_id(self, patient_id):
        patient = Patient.objects(id=patient_id).get()
        json_data = json.loads(patient.to_json())
        return json_data
    

    # done
    def add_patient(self, current_doctor, first_name, second_name, address, contact_number, assigned_doctor_name, next_of_kin1_first_name, next_of_kin1_second_name, next_of_kin2_first_name, next_of_kin2_second_name, severity, medical_data):
        return Patient (
            assigned_doctor = current_doctor,
            first_name = first_name,
            second_name = second_name,
            address = address,
            contact_number = contact_number,
            assigned_doctor_name = assigned_doctor_name,
            next_of_kin1_first_name = next_of_kin1_first_name,
            next_of_kin1_second_name = next_of_kin1_second_name,
            next_of_kin2_first_name = next_of_kin2_first_name,
            next_of_kin2_second_name = next_of_kin2_second_name,
            severity = severity,
            medical_data = medical_data
        ).save()

    # done
    def delete_patient(self, patient_id):
        patient = None
        try:
            patient = Patient.objects(id=patient_id).get()
            return patient.delete()
        except:
            patient = None
            return "No patient exist"
    # todo
    def update_patient_details(self, patient_id, first_name, second_name, address, contact_number, next_of_kin1_first_name, next_of_kin1_second_name, next_of_kin2_first_name, next_of_kin2_second_name):
        return Patient.objects(id=patient_id).update(
            first_name = first_name,
            second_name = second_name,
            address = address,
            contact_number = contact_number,
            next_of_kin1_first_name = next_of_kin1_first_name,
            next_of_kin1_second_name = next_of_kin1_second_name,
            next_of_kin2_first_name = next_of_kin2_first_name,
            next_of_kin2_second_name = next_of_kin2_second_name
        )

    # done
    def assign_severity(self, patient_id, severity):
        return Patient.objects(id=patient_id).update(severity = severity)

    def check_the_doctor_collection_size(self):
        return Doctor.objects.count()

    def check_the_patients_collection_size(self):
        return Patient.objects.count()
    
    def check_the_nurse_collection_size(self):
        return Nurse.objects.count()

    def delete_doctor_collection(self):
        return Doctor.objects.delete()
    
    def delete_patients_collection(self):
        return Patient.objects.delete()
    
    def delete_nurse_collection(self):
        return Nurse.objects.delete()

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

        