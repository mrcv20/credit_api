from flask import json
import pytest
from myapp.run import app


@pytest.fixture
def client():
    with app.app_context():
        with app.test_client() as client:
            yield client

def test_for_sucessfully_api_doc(client):
    response = client.get('http://127.0.0.1:5000/api/v1/')
    assert b'API' in response.data 


def test_for_not_allowed_api(client):
    response = client.post('http://127.0.0.1:5000/api/v1/')    
    assert b'The method is not allowed for the requested URL' in response.data


def test_for_sucessfully_payload_post(client):
    response = client.post('http://localhost:5000/api/v1/credito/', 
    json={"CPF": "string",
    "idade": 18,
    "nome": "marcos",
    "valor_solicitado": 1000})
    assert b'Pedido enviado' in response.data 


def test_for_not_allowed_payload_get(client):
    response = client.get('http://127.0.0.1:5000/api/v1/credito/',
    json={"CPF": "string",
    "idade": 18,
    "nome": "marcos",
    "valor_solicitado": 1000})
    assert b'The method is not allowed for the requested URL' in response.data

# def test_for_consult_ticket(client):
#     response = client.get('http://127.0.0.1:5000/api/v1/credito/b45d5409-f614-41ff-9189-1221f2e2b761')    
#     assert json={"status": ""} in response.data


