import pytest
import json
import sys
sys.path.insert(1, './../../Models')
from operations import Operations

class TestVisualisationControllers:
    @classmethod
    def setup_class(cls):
        """ setup any state specific to the execution of the given class (which
        usually contains tests).
        """
        cls.x_axis_value = 1
        cls.x_axis_name = 'sex'
        cls.y_axis_value = 0
        cls.y_axis_name = 'sex'
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

  
    @classmethod
    def teardown_class(cls):
        """ teardown any state that was previously setup with a call to
        setup_class.
        """
        ""
        cls.x_axis_value = None
        cls.x_axis_name = None
        cls.y_axis_value = None
        cls.y_axis_name = None
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
    
 
      
    def test_condition_visualisation_with_wrong_inputs(self, client, auth):
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
        
        headers = {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Credentials': True
        }
        payload = {'xValue': None, 'xAttr': 'Choose...', 'yValue': None, 'yAttr': 'Choose...'}
        data = json.dumps(payload)
        url = '/api/condition-visualisation'
        res = client.post(url, data=data, headers=headers)
        assert res.status_code == 400
        assert b'Please choose appropriate medical data option in the drop down(s).' in res.data

       