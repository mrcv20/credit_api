import os
import tempfile
import pytest
from myapp import create_app


@pytest.fixture
def client():
    
    app = create_app()
    app.config['TESTING'] = True
    with app.app_context():
        with app.test_client() as client:
            yield client

def test_url_response_404(client):
    response = client.get('/') # data
    assert b'Not Found' in response.data # then    

def test_for_empty_parameters(client):
    response = client.post('http://127.0.0.1:5000/api/pedido-credito', json={}) # data
    assert b'' in response.data # then

def test_for_sucessfuly_query_request(client):
    response = client.get('http://127.0.0.1:5000/api/consulta-pedidos') # data
    assert b'\n' in response.data # then
