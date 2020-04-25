import pytest
import json
import sys
sys.path.insert(1, './../../Models')
from operations import Operations

class TestPatientsControllers:
    @classmethod
    def setup_class(cls):
        """ setup any state specific to the execution of the given class (which
        usually contains tests).
        """
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
        cls.patient_first_name = 'yo'
        cls.patient_second_name = 'suts'
        cls.address = '54 Middle Abbey Street Dublin1'
        cls.contact_number = '0860234455'
        cls.next_of_kin1_first_name = 'yo'
        cls.next_of_kin1_second_name = 'suts'
        cls.next_of_kin2_first_name = 'yo'
        cls.next_of_kin2_second_name = 'suts'
        cls.new_patient_first_name = 'new'
        cls.new_patient_second_name = 'new'
        cls.new_address = 'new'
        cls.new_contact_number = 'new'
        cls.new_next_of_kin1_first_name = 'new'
        cls.new_next_of_kin1_second_name = 'new'
        cls.new_next_of_kin2_first_name = 'new'
        cls.new_next_of_kin2_second_name = 'new'
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
        cls.ops = Operations()

  
    @classmethod
    def teardown_class(cls):
        """ teardown any state that was previously setup with a call to
        setup_class.
        """
        ""

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
        if cls.ops.check_the_doctor_collection_size() > 0:
            cls.ops.delete_doctor_collection()
        
        if cls.ops.check_the_patients_collection_size() > 0:
            cls.ops.delete_patients_collection()
        
        if cls.ops.check_the_nurse_collection_size() > 0:
            cls.ops.delete_nurse_collection()
        
        cls.ops = None
    
 
    # Happy paths
    def test_view_patients_using_doctor_id(self, client, auth):
        headers = {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Credentials': True
        }
        payload = {'employee_id': self.doctor_id, 'job_role' : self.doctor_job_role ,'password' : self.password, 'confirm_password' : self.confirm_password, 'first_name' : self.first_name, 'second_name' : self.second_name, 'contact_number' : self.contact_number, 'room': self.room, 'ward': self.ward}
        data = json.dumps(payload)
        url = '/api/register'
        client.post(url, data=data, headers=headers)

        diagnosis_payload = {'first_name': self.patient_first_name, 'second_name': self.patient_second_name, 'address': self.address, 'contact_number': self.contact_number, 'next_of_kin1_first_name' : self.next_of_kin1_first_name, 'next_of_kin1_second_name': self.next_of_kin1_second_name, 'next_of_kin2_first_name': self.next_of_kin2_first_name, 'next_of_kin2_second_name': self.next_of_kin2_second_name, 'age' : self.age, 'gender': self.sex, 'cp' : self.cp, 'trestbps' : self.trestbps, 'chol': self.chol, 'fbs' : self.fbs, 'restecg' : self.restecg, 'thalach': self.thalach, 'exang' : self.exang, 'oldpeak' : self.oldpeak, 'slope': self.slope, 'ca': self.ca, 'thal': self.thal}
        diagnosis_data = json.dumps(diagnosis_payload)
        diagnosis_url = '/api/diagnosis'
        res = client.post(diagnosis_url, data=diagnosis_data, headers=headers)

        view_patients_url = '/api/patients'
        view_patients_response = client.get(view_patients_url, headers=headers)
        assert view_patients_response.status_code == 200
        assert b'yo' in view_patients_response.data
    
    def test_view_patients_using_nurse_id(self, client, auth):
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

        view_patients_url = '/api/patients'
        view_patients_response = client.get(view_patients_url, headers=headers)
        assert view_patients_response.status_code == 200
        assert b'yo' in view_patients_response.data
    
    def test_assigning_severity(self, client, auth):
        auth.login()
        headers = {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Credentials': True
        }
        patients = self.ops.get_every_patients()
        patient_id = patients[0]['_id']['$oid']
        severity_payload = {'patientId': patient_id, 'severity' : '2'}
        severity_data = json.dumps(severity_payload)
        severity_url = '/api/assign-severity'
        severity_response = client.post(severity_url, data=severity_data, headers=headers)
        assert severity_response.status_code == 200
        assert b'The patient has been assigned with severity.' in severity_response.data
    
    def test_view_patients_with_severity(self, client, auth):
        auth.logout()
        auth.login()
        headers = {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Credentials': True
        }
        view_patients_with_severity_url = '/api/patients?q=waiting-list'
        view_patients_with_severity_url_response = client.get(view_patients_with_severity_url, headers=headers)
        assert view_patients_with_severity_url_response.status_code == 200
        assert b'yo' in view_patients_with_severity_url_response.data
    
    def test_view_individual_patient_using_doctor_id(self, client, auth):
        auth.logout()
        auth.login()
        headers = {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Credentials': True
        }
        patients = self.ops.get_every_patients()
        patient_id = patients[0]['_id']['$oid']
        view_patient_url = '/api/patient?id=' + patient_id
        view_patient_url_response = client.get(view_patient_url, headers=headers)
        assert view_patient_url_response.status_code == 200
        assert b'yo' in view_patient_url_response.data
    
    def test_view_individual_patient_using_nurse_id(self, client, auth):
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

        auth.login_nurse()

        patients = self.ops.get_every_patients()
        patient_id = patients[0]['_id']['$oid']
        view_patient_url = '/api/patient?id=' + patient_id
        view_patient_url_response = client.get(view_patient_url, headers=headers)
        assert view_patient_url_response.status_code == 200
        assert b'yo' in view_patient_url_response.data
    
    def test_update_individual_patient_using_doctor_id(self, client, auth):
        auth.logout()
        auth.login()
        headers = {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Credentials': True
        }

        patients = self.ops.get_every_patients()
        patient_id = patients[0]['_id']['$oid']

        update_payload = {'first_name': self.new_patient_first_name, 'second_name': self.new_patient_second_name, 'address': self.new_address, 'contact_number': self.contact_number, 'next_of_kin1_first_name' : self.new_next_of_kin1_first_name, 'next_of_kin1_second_name': self.new_next_of_kin1_second_name, 'next_of_kin2_first_name': self.new_next_of_kin2_first_name, 'next_of_kin2_second_name': self.new_next_of_kin2_second_name}

        update_data = json.dumps(update_payload)
        update_patient_url = '/api/patient?id=' + patient_id + '&q=update'
        update_patient_url_response = client.post(update_patient_url, data=update_data, headers=headers)
        assert update_patient_url_response.status_code == 200
        assert b'Details updated successfully.' in update_patient_url_response.data

    # Unhappy path
    def test_view_patient_without_logging_in(self, client, auth):
        auth.logout()
        headers = {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Credentials': True
        }
        patient_id = '1234'
        view_patient_url = '/api/patients?id=' + patient_id
        view_patient_url_response = client.get(view_patient_url, headers=headers)
        assert view_patient_url_response.status_code == 401
        assert b'Please log in.' in view_patient_url_response.data

    
    def test_view_patients_without_logging_in(self, client, auth):
        auth.logout()
        headers = {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Credentials': True
        }
        view_patients_url = '/api/patients'
        view_patients_response = client.get(view_patients_url, headers=headers)
        assert view_patients_response.status_code == 401
        assert b'Please log in.' in view_patients_response.data
    
    def test_assign_severity_without_logging_in(self, client, auth):
        auth.logout()
        headers = {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Credentials': True
        }
        patient_id = '1234'
        severity_payload = {'patientId': patient_id, 'severity' : '2'}
        severity_data = json.dumps(severity_payload)
        severity_url = '/api/assign-severity'
        severity_response = client.post(severity_url, data=severity_data, headers=headers)
        assert severity_response.status_code == 401
        assert b'Please log in.' in severity_response.data

    def test_assign_severity_without_access(self, client, auth):
        auth.logout()
        headers = {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Credentials': True
        }

        auth.login_nurse()

        patient_id = '1234'
        severity_payload = {'patientId': patient_id, 'severity' : '2'}
        severity_data = json.dumps(severity_payload)
        severity_url = '/api/assign-severity'
        severity_response = client.post(severity_url, data=severity_data, headers=headers)
        assert severity_response.status_code == 403
        assert b'You do not have access to this functionality.' in severity_response.data


    def test_assigning_severity_with_wrong_severity_level(self, client, auth):
        auth.login()
        headers = {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Credentials': True
        }
        patients = self.ops.get_every_patients()
        patient_id = patients[0]['_id']['$oid']
        severity_payload = {'patientId': patient_id, 'severity' : '6'}
        severity_data = json.dumps(severity_payload)
        severity_url = '/api/assign-severity'
        severity_response = client.post(severity_url, data=severity_data, headers=headers)
        assert severity_response.status_code == 400
        assert b'The severity level ranging from 0 to 5. Please assign an appropriate severity level.' in severity_response.data
    

    def test_update_individual_patient_with_incorrect_information(self, client, auth):
        auth.logout()
        auth.login()
        headers = {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Credentials': True
        }

        patient_id = '12222'

        update_payload = {'first_name': self.new_patient_first_name, 'second_name': self.new_patient_second_name, 'address': self.new_address, 'contact_number': self.new_contact_number, 'next_of_kin1_first_name' : self.new_next_of_kin1_first_name, 'next_of_kin1_second_name': self.new_next_of_kin1_second_name, 'next_of_kin2_first_name': self.new_next_of_kin2_first_name, 'next_of_kin2_second_name': self.new_next_of_kin2_second_name}

        update_data = json.dumps(update_payload)
        update_patient_url = '/api/patient?id=' + patient_id + '&q=update'
        update_patient_url_response = client.post(update_patient_url, data=update_data, headers=headers)
        assert update_patient_url_response.status_code == 400
        assert b'Please provide an appropriate information.' in update_patient_url_response.data
    
    def test_update_individual_patient_with_wrong_query(self, client, auth):
        auth.logout()
        auth.login()
        headers = {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Credentials': True
        }

        patient_id = '12222'

        update_payload = {'first_name': self.new_patient_first_name, 'second_name': self.new_patient_second_name, 'address': self.new_address, 'contact_number': self.new_contact_number, 'next_of_kin1_first_name' : self.new_next_of_kin1_first_name, 'next_of_kin1_second_name': self.new_next_of_kin1_second_name, 'next_of_kin2_first_name': self.new_next_of_kin2_first_name, 'next_of_kin2_second_name': self.new_next_of_kin2_second_name}

        update_data = json.dumps(update_payload)
        update_patient_url = '/api/patient?id=' + patient_id + '&q=wrongQuery'
        update_patient_url_response = client.post(update_patient_url, data=update_data, headers=headers)
        assert update_patient_url_response.status_code == 404
        assert b'Operation not supported.' in update_patient_url_response.data
    
    def test_delete_patient_with_incorrect_operation(self, client, auth):
        auth.logout()
        auth.login()
        headers = {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Credentials': True
        }
     
        patient_id = '12345'
        delete_payload = {'patient_id' : patient_id}

        delete_data = json.dumps(delete_payload)
        delete_patient_url = '/api/patient?id=' + patient_id + '&q=wrongQuery'
        delete_patient_url_response = client.delete(delete_patient_url, data=delete_data, headers=headers)
        assert delete_patient_url_response.status_code == 404
        assert b'Operation not supported.' in delete_patient_url_response.data
    
        
    def test_delete_patient(self, client, auth):
        auth.logout()
        auth.login()
        headers = {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Credentials': True
        }
        patients = self.ops.get_every_patients()
        patient_id = patients[0]['_id']['$oid']
        delete_payload = {'patient_id' : patient_id}

        delete_data = json.dumps(delete_payload)
        delete_patient_url = '/api/patient?id=' + patient_id + '&q=delete'
        delete_patient_url_response = client.delete(delete_patient_url, data=delete_data, headers=headers)
        assert delete_patient_url_response.status_code == 200
        assert b'Selected patient has been deleted.' in delete_patient_url_response.data
    


       