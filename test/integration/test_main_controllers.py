import pytest
import json
import sys
sys.path.insert(1, './../../Models')
from operations import Operations
from random import choice
from string import ascii_lowercase


class TestMainControllers:
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
        cls.ops = Operations()
        cls.one_hundred_string_length = ''.join(choice(ascii_lowercase) for i in range(102))
        

    @classmethod
    def teardown_class(cls):
        """ teardown any state that was previously setup with a call to
        setup_class.
        """
        ""
        if cls.ops.check_the_doctor_collection_size() > 0:
            cls.ops.delete_doctor_collection()
        
        if cls.ops.check_the_patients_collection_size() > 0:
            cls.ops.delete_patients_collection()
        
        if cls.ops.check_the_nurse_collection_size() > 0:
            cls.ops.delete_nurse_collection()
        
        cls.ops = None
    

    # Happy paths
    def test_home(self, client):
        res = client.get('/')
        assert b'HDDT backend server started.' in res.data

    def test_register_doctor(self, client):
        headers = {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Credentials': True
        }
        payload = {'employee_id': self.doctor_id, 'job_role' : self.doctor_job_role ,'password' : self.password, 'confirm_password' : self.confirm_password, 'first_name' : self.first_name, 'second_name' : self.second_name, 'contact_number' : self.contact_number, 'room': self.room, 'ward': self.ward}
        data = json.dumps(payload)
        url = '/api/register'
        res = client.post(url, data=data, headers=headers)
        assert res.status_code == 200

    def test_register_nurse(self, client):
        headers = {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Credentials': True
        }
        payload = {'employee_id': self.nurse_id, 'job_role' : self.nurse_job_role ,'password' : self.password, 'confirm_password' : self.confirm_password, 'first_name' : self.first_name, 'second_name' : self.second_name, 'contact_number' : self.contact_number, 'room': self.room, 'ward': self.ward}
        data = json.dumps(payload)
        url = '/api/register'
        res = client.post(url,data=data, headers=headers)
        print(res.data)
        assert res.status_code == 200

    def test_login(self, client):
        headers = {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Credentials': True
        }
        payload = {'employee_id': self.doctor_id, 'password' : self.password}
        data = json.dumps(payload)
        url = '/api/login'
        res = client.post(url, data=data, headers=headers)
        print(res.data)
        assert res.status_code == 200

    def test_logout(self, client, auth):
        auth.login()
        url = '/api/logout'
        res = client.get(url)
        print(res.data)
        assert res.status_code == 200
    
    # Unhappy paths
    def test_register_with_existing_employee_id(self, client):
        headers = {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Credentials': True
        }
        payload = {'employee_id': self.doctor_id, 'job_role' : self.doctor_job_role ,'password' : self.password, 'confirm_password' : self.confirm_password, 'first_name' : self.first_name, 'second_name' : self.second_name, 'contact_number' : self.contact_number, 'room': self.room, 'ward': self.ward}
        data = json.dumps(payload)
        url = '/api/register'
        res = client.post(url,data=data, headers=headers)
        print(res.data)
        assert res.status_code == 400
        assert b'The employee ID already exists.' in res.data

    def test_register_with_wrong_confirm_password(self, client):
        headers = {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Credentials': True
        }
        payload = {'employee_id': self.new_doctor_id, 'job_role' : self.doctor_job_role ,'password' : self.password, 'confirm_password' : '11111111', 'first_name' : self.first_name, 'second_name' : self.second_name, 'contact_number' : self.contact_number, 'room': self.room, 'ward': self.ward}
        data = json.dumps(payload)
        url = '/api/register'
        res = client.post(url,data=data, headers=headers)
        print(res.data)
        assert res.status_code == 400
        assert b'Password and comfirm password are not the same.' in res.data

    def test_register_with_wrong_password_format(self, client):
        headers = {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Credentials': True
        }
        payload = {'employee_id': self.new_doctor_id, 'job_role' : self.doctor_job_role ,'password' : '123456$', 'confirm_password' : '123456$', 'first_name' : self.first_name, 'second_name' : self.second_name, 'contact_number' : self.contact_number, 'room': self.room, 'ward': self.ward}
        data = json.dumps(payload)
        url = '/api/register'
        res = client.post(url,data=data, headers=headers)
        print(res.data)
        assert res.status_code == 400
        assert b'Password must contain the minimum of 8 characters with the combination of letters or numbers.' in res.data
    
    def test_register_with_wrong_contact_number_format(self, client):
        headers = {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Credentials': True
        }
        payload = {'employee_id': self.new_doctor_id, 'job_role' : self.doctor_job_role ,'password' : self.password, 'confirm_password' : self.confirm_password, 'first_name' : self.first_name, 'second_name' : self.second_name, 'contact_number' : 'a09882233443', 'room': self.room, 'ward': self.ward}
        data = json.dumps(payload)
        url = '/api/register'
        res = client.post(url,data=data, headers=headers)
        print(res.data)
        assert res.status_code == 400
        assert b'The contact number must contain only digits and follow the Irish phone number standard ie. 08xxxxxxxx.' in res.data
    
    def test_register_with_wrong_room_number_format(self, client):
        headers = {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Credentials': True
        }
        payload = {'employee_id': self.new_doctor_id, 'job_role' : self.doctor_job_role ,'password' : self.password, 'confirm_password' : self.confirm_password, 'first_name' : self.first_name, 'second_name' : self.second_name, 'contact_number' : self.contact_number, 'room': '12344', 'ward': self.ward}
        data = json.dumps(payload)
        url = '/api/register'
        res = client.post(url,data=data, headers=headers)
        print(res.data)
        assert res.status_code == 400
        assert b'Room number must be less than 3 characters.' in res.data

    def test_register_with_wrong_ward_format(self, client):
        headers = {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Credentials': True
        }
        payload = {'employee_id': self.new_doctor_id, 'job_role' : self.doctor_job_role ,'password' : self.password, 'confirm_password' : self.confirm_password, 'first_name' : self.first_name, 'second_name' : self.second_name, 'contact_number' : self.contact_number, 'room': self.room, 'ward': 'eastwest12345'}
        data = json.dumps(payload)
        url = '/api/register'
        res = client.post(url,data=data, headers=headers)
        print(res.data)
        assert res.status_code == 400
        assert b'Please provide an appropriate  ward location.' in res.data

    def test_register_with_wrong_first_second_name_format(self, client):
        headers = {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Credentials': True
        }
        payload = {'employee_id': self.new_doctor_id, 'job_role' : self.doctor_job_role ,'password' : self.password, 'confirm_password' : self.confirm_password, 'first_name' : self.one_hundred_string_length, 'second_name' : self.one_hundred_string_length, 'contact_number' : self.contact_number, 'room': self.room, 'ward': self.ward}
        data = json.dumps(payload)
        url = '/api/register'
        res = client.post(url,data=data, headers=headers)
        print(res.data)
        assert res.status_code == 400
        assert b'The minimum length of first and second name characters must not exceed 40 letters.' in res.data
    
    def test_register_with_wrong_employee_id_format(self, client):
        headers = {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Credentials': True
        }
        payload = {'employee_id': 'a123456789$', 'job_role' : self.doctor_job_role ,'password' : self.password, 'confirm_password' : self.confirm_password, 'first_name' : self.first_name, 'second_name' : self.second_name, 'contact_number' : self.contact_number, 'room': self.room, 'ward': self.ward}
        data = json.dumps(payload)
        url = '/api/register'
        res = client.post(url,data=data, headers=headers)
        print(res.data)
        assert res.status_code == 400
        assert b'The Employee ID must be less than 8 characters with the combination of letters or numbers.' in res.data
    
    def test_register_with_wrong_job_role(self, client):
        headers = {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Credentials': True
        }
        payload = {'employee_id': self.new_doctor_id, 'job_role' : 'Teacher','password' : self.password, 'confirm_password' : self.confirm_password, 'first_name' : self.first_name, 'second_name' : self.second_name, 'contact_number' : self.contact_number, 'room': self.room, 'ward': self.ward}
        data = json.dumps(payload)
        url = '/api/register'
        res = client.post(url,data=data, headers=headers)
        print(res.data)
        assert res.status_code == 400
        assert b'Please provide an appropriate job role.' in res.data

    def test_login_doctor_with_wrong_combinations(self, client, auth):
        auth.logout()
        headers = {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Credentials': True
        }
        payload = {'employee_id': self.doctor_id, 'password' : '1234556y'}
        data = json.dumps(payload)
        url = '/api/login'
        res = client.post(url, data=data, headers=headers)
        print(res.data)
        assert res.status_code == 400
        assert b'Invalid combinations. Please try again.' in res.data
    
    def test_login_nurse_with_wrong_combinations(self, client, auth):
        auth.logout()
        headers = {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Credentials': True
        }
        payload = {'employee_id': self.nurse_id, 'password' : '1234556y'}
        data = json.dumps(payload)
        url = '/api/login'
        res = client.post(url, data=data, headers=headers)
        print(res.data)
        assert res.status_code == 400
        assert b'Invalid combinations. Please try again.' in res.data

    def test_login_with_no_such_account_exists(self, client, auth):
        auth.logout()
        headers = {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Credentials': True
        }
        payload = {'employee_id': self.new_doctor_id, 'password' : '1234556y'}
        data = json.dumps(payload)
        url = '/api/login'
        res = client.post(url, data=data, headers=headers)
        print(res.data)
        assert res.status_code == 400
        assert b'No account exists with the given employee ID. Please register a new user account.' in res.data
    
    def test_logout_when_no_session(self, auth, client):
        auth.logout()
        res = client.get('/api/logout')
        assert res.status_code == 400
        assert b'You need to log in first.' in res.data