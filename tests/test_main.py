from curses import panel
from urllib import response

import requests
from app.main import app, knowledge_panel
from fastapi.testclient import TestClient

client = TestClient(app)


def test_hello():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Hello from facets-knowledge-panels! Tip: open /docs for documentation"}


def test_knowledge_panel():
    response = client.get("/knowledge_panel")
    assert response.status_code == 422


def test_knowledge_panel_badendpoint():
    response = client.get("/knowledge_panel_bad")
    assert response.status_code == 404

def test_knowledge_panel_with_actegory():
    assert knowledge_panel(facet_name="category") == {"knowledge_panels": [{'hunger-game': {'elements': [{'element_type': 'text', 'text_element': {
        'html': "'<p><a href='https://hunger.openfoodfacts.org/?type=catergory'></a></p>\n'"}}]}}]}