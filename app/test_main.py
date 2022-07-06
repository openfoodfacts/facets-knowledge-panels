from fastapi.testclient import TestClient
import requests
from .main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/brand/president")
    assert response.status_code == 200
    assert response.json() == {"knowledge_panels": []}

def test_read_root_bad():
    response = client.get("/brand/bad_facet_value")
    assert response.status_code == 404
    assert response.json() == {'detail': 'Not Found'}