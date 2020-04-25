import pytest
import json
import sys
sys.path.insert(1, './../../Models')
from operations import Operations
from random import choice
from string import ascii_lowercase

class TestDiagnosisControllers:
    @classmethod
    def setup_class(cls):
        """ setup any state specific to the execution of the given class (which
        usually contains tests).
        """
        cls.ops = Operations()
        cls.patient_first_name = "yo"
        cls.patient_second_name = "suts"
        cls.address = "54 Middle Abbey Street Dublin1"
        cls.contact_number = "0860234455"
        cls.next_of_kin1_first_name = "yo"
        cls.next_of_kin1_second_name = "suts"
        cls.next_of_kin2_first_name = "yo"
        cls.next_of_kin2_second_name = "suts"
        cls.doctor_id = 'testd'
        cls.new_doctor_id = "newTestd"
        cls.doctor_job_role = 'Doctor'
        cls.nurse_id = 'testn'
        cls.nurse_job_role = 'Nurse'
        cls.password = 'test1234'
        cls.confirm_password = 'test1234'
        cls.first_name = 'test'
        cls.second_name = 'test'
        cls.contact_number = '0876654433'
        cls.room = '123'
        cls.ward = 'east1'
        cls.age = '63'
        cls.sex = '1'
        cls.cp = '1'
        cls.trestbps = '145'
        cls.chol = '233'
        cls.fbs = '1'
        cls.restecg = '2'
        cls.thalach = '150'
        cls.exang = '0'
        cls.oldpeak = '2.3'
        cls.slope = '3'
        cls.ca = '0'
        cls.thal = '0'
        cls.one_hundred_string_length = ''.join(choice(ascii_lowercase) for i in range(102))
        cls.choose = 'Choose...'

    @classmethod
    def teardown_class(cls):
        """ teardown any state that was previously setup with a call to
        setup_class.
        """
        ""
        cls.patient_first_name = None
        cls.patient_second_name = None
        cls.address = None
        cls.contact_number = None
        cls.next_of_kin1_first_name = None
        cls.next_of_kin1_second_name = None
        cls.next_of_kin2_first_name = None
        cls.next_of_kin2_second_name = None
        cls.doctor_id = None
        cls.new_doctor_id = None
        cls.doctor_job_role = None
        cls.nurse_id = None
        cls.nurse_job_role = None
        cls.password = None
        cls.confirm_password = None
        cls.first_name = None
        cls.second_name = None
        cls.contact_number = None
        cls.room = None
        cls.ward = None
        cls.age = None
        cls.sex = None
        cls.cp = None
        cls.trestbps = None
        cls.chol = None
        cls.fbs = None
        cls.restecg = None
        cls.thalach = None
        cls.exang = None
        cls.oldpeak = None
        cls.slope = None
        cls.ca = None
        cls.thal = None
        cls.one_hundred_string_length = None
        cls.choose = None

        if cls.ops.check_the_doctor_collection_size() > 0:
            cls.ops.delete_doctor_collection()
        
        if cls.ops.check_the_patients_collection_size() > 0:
            cls.ops.delete_patients_collection()
        
        if cls.ops.check_the_nurse_collection_size() > 0:
            cls.ops.delete_nurse_collection()
        
        cls.ops = None
 
      
    # Happy path
    def test_patients_diagnosis(self, client, auth):
        headers = {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Credentials': True
        }
        payload = {'employee_id': self.doctor_id, 'job_role' : self.doctor_job_role ,'password' : self.password, 'confirm_password' : self.confirm_password, 'first_name' : self.first_name, 'second_name' : self.second_name, 'contact_number' : self.contact_number, 'room': self.room, 'ward': self.ward}
        data = json.dumps(payload)
        url = '/api/register'
        client.post(url, data=data, headers=headers)

        auth.login()
        
        diagnosis_headers = {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Credentials': True
        }
        diagnosis_payload = {'first_name': self.patient_first_name, 'second_name': self.patient_second_name, 'address': self.address, 'contact_number': self.contact_number, 'next_of_kin1_first_name' : self.next_of_kin1_first_name, 'next_of_kin1_second_name': self.next_of_kin1_second_name, 'next_of_kin2_first_name': self.next_of_kin2_first_name, 'next_of_kin2_second_name': self.next_of_kin2_second_name, 'age' : self.age, 'gender': self.sex, 'cp' : self.cp, 'trestbps' : self.trestbps, 'chol': self.chol, 'fbs' : self.fbs, 'restecg' : self.restecg, 'thalach': self.thalach, 'exang' : self.exang, 'oldpeak' : self.oldpeak, 'slope': self.slope, 'ca': self.ca, 'thal': self.thal}
        diagnosis_data = json.dumps(diagnosis_payload)
        diagnosis_url = '/api/diagnosis'
        res = client.post(diagnosis_url, data=diagnosis_data, headers=diagnosis_headers)
        assert res.status_code == 200
        assert b'first_name' in res.data
        assert b'second_name' in res.data
        assert b'accuracy' in res.data
        assert b'medical_details' in res.data
        assert b'personal_details' in res.data
        assert b'models_details' in res.data
    
    # Unhappy paths
    def test_patients_diagnosis_without_login(self, client, auth):
        diagnosis_headers = {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Credentials': True
        }
        diagnosis_payload = {'first_name': self.patient_first_name, 'second_name': self.patient_second_name, 'address': self.address, 'contact_number': self.contact_number, 'next_of_kin1_first_name' : self.next_of_kin1_first_name, 'next_of_kin1_second_name': self.next_of_kin1_second_name, 'next_of_kin2_first_name': self.next_of_kin2_first_name, 'next_of_kin2_second_name': self.next_of_kin2_second_name, 'age' : self.age, 'gender': self.sex, 'cp' : self.cp, 'trestbps' : self.trestbps, 'chol': self.chol, 'fbs' : self.fbs, 'restecg' : self.restecg, 'thalach': self.thalach, 'exang' : self.exang, 'oldpeak' : self.oldpeak, 'slope': self.slope, 'ca': self.ca, 'thal': self.thal}
        diagnosis_data = json.dumps(diagnosis_payload)
        diagnosis_url = '/api/diagnosis'
        res = client.post(diagnosis_url, data=diagnosis_data, headers=diagnosis_headers)
        assert res.status_code == 400
        assert b'Please log in.' in res.data
    
    def test_patients_diagnosis_without_access(self, client, auth):
        auth.logout()

        headers = {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Credentials': True
        }
        payload = {'employee_id': self.nurse_id, 'job_role' : self.nurse_job_role ,'password' : self.password, 'confirm_password' : self.confirm_password, 'first_name' : self.first_name, 'second_name' : self.second_name, 'contact_number' : self.contact_number, 'room': self.room, 'ward': self.ward}
        data = json.dumps(payload)
        url = '/api/register'
        client.post(url, data=data, headers=headers)

        diagnosis_headers = {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Credentials': True
        }

        diagnosis_payload = {'first_name': self.patient_first_name, 'second_name': self.patient_second_name, 'address': self.address, 'contact_number': self.contact_number, 'next_of_kin1_first_name' : self.next_of_kin1_first_name, 'next_of_kin1_second_name': self.next_of_kin1_second_name, 'next_of_kin2_first_name': self.next_of_kin2_first_name, 'next_of_kin2_second_name': self.next_of_kin2_second_name, 'age' : self.age, 'gender': self.sex, 'cp' : self.cp, 'trestbps' : self.trestbps, 'chol': self.chol, 'fbs' : self.fbs, 'restecg' : self.restecg, 'thalach': self.thalach, 'exang' : self.exang, 'oldpeak' : self.oldpeak, 'slope': self.slope, 'ca': self.ca, 'thal': self.thal}
        diagnosis_data = json.dumps(diagnosis_payload)
        diagnosis_url = '/api/diagnosis'
        res = client.post(diagnosis_url, data=diagnosis_data, headers=diagnosis_headers)
        assert res.status_code == 403
        assert b'You do not have access to this functionality.' in res.data
    
    def test_patients_diagnosis_with_wrong_information(self, client, auth):
        headers = {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Credentials': True
        }
        payload = {'employee_id': self.new_doctor_id, 'job_role' : self.doctor_job_role ,'password' : self.password, 'confirm_password' : self.confirm_password, 'first_name' : self.first_name, 'second_name' : self.second_name, 'contact_number' : self.contact_number, 'room': self.room, 'ward': self.ward}
        data = json.dumps(payload)
        url = '/api/register'
        client.post(url, data=data, headers=headers)

        auth.login()
        
        diagnosis_headers = {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Credentials': True
        }
        diagnosis_payload = {'first_name': self.one_hundred_string_length, 'second_name': self.one_hundred_string_length, 'address': self.one_hundred_string_length, 'contact_number': self.contact_number, 'next_of_kin1_first_name' : self.one_hundred_string_length, 'next_of_kin1_second_name': self.one_hundred_string_length, 'next_of_kin2_first_name': self.one_hundred_string_length, 'next_of_kin2_second_name': self.one_hundred_string_length, 'age' : '', 'gender': self.sex, 'cp' : self.cp, 'trestbps' : '', 'chol': '', 'fbs' : self.fbs, 'restecg' : self.restecg, 'thalach': '', 'exang' : self.exang, 'oldpeak' : self.oldpeak, 'slope': self.slope, 'ca': self.ca, 'thal': self.thal}
        diagnosis_data = json.dumps(diagnosis_payload)
        diagnosis_url = '/api/diagnosis'
        res = client.post(diagnosis_url, data=diagnosis_data, headers=diagnosis_headers)
        assert res.status_code == 400
        assert b'Please provide an appropriate information.' in res.data
    
    def test_patients_diagnosis_witout_choosing_data(self, client, auth):
        auth.login()
        
        diagnosis_headers = {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Credentials': True
        }
        diagnosis_payload = {'first_name': self.patient_first_name, 'second_name': self.patient_second_name, 'address': self.address, 'contact_number': self.contact_number, 'next_of_kin1_first_name' : self.next_of_kin1_first_name, 'next_of_kin1_second_name': self.next_of_kin1_second_name, 'next_of_kin2_first_name': self.next_of_kin2_first_name, 'next_of_kin2_second_name': self.next_of_kin2_second_name, 'age' : self.choose, 'gender': self.choose, 'cp' : self.choose, 'trestbps' : self.choose, 'chol': self.choose, 'fbs' : self.choose, 'restecg' : self.choose, 'thalach': self.choose, 'exang' : self.choose, 'oldpeak' : self.choose, 'slope': self.choose, 'ca': self.choose, 'thal': self.choose}
        diagnosis_data = json.dumps(diagnosis_payload)
        diagnosis_url = '/api/diagnosis'
        res = client.post(diagnosis_url, data=diagnosis_data, headers=diagnosis_headers)
        assert res.status_code == 400
        assert b'Please choose appropriate medical data option in the drop down(s).' in res.data
       