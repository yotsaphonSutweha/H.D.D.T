import os
import pytest
import sys
import json
sys.path.insert(1, './../../')
from Controllers import create_app

@pytest.fixture
def app():
    app = create_app(test_config=True)
    return app

@pytest.fixture
def client(app):
    return app.test_client()

class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, employee_id='testd', password='test1234'):
        headers = {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Credentials': True
        }
        payload = {'employee_id': employee_id, 'password' : password}
        data = json.dumps(payload)
        url = '/api/login'
        res = self._client.post(url, data=data, headers=headers)
        return res
    
    def login_nurse(self, employee_id='testn', password='test1234'):
        headers = {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Credentials': True
        }
        payload = {'employee_id': employee_id, 'password' : password}
        data = json.dumps(payload)
        url = '/api/login'
        res = self._client.post(url, data=data, headers=headers)
        return res
    
    def logout(self):
        return self._client.get('/api/logout')

@pytest.fixture
def auth(client):
    return AuthActions(client)
  