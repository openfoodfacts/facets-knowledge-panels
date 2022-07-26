import app.main
from curses import panel
from urllib import response
import json
import requests
from app.main import app, knowledge_panel
from .test_utils import mock_get_factory
from fastapi.testclient import TestClient

client = TestClient(app)


def test_hello():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Hello from facets-knowledge-panels! Tip: open /docs for documentation"
    }


def test_knowledge_panel():
    response = client.get("/knowledge_panel?facet_name=origin")
    assert response.status_code == 200


def test_knowledge_panel_badendpoint():
    response = client.get("/knowledge_panel_bad")
    assert response.status_code == 404


def test_knowledge_panel_with_facet():
    response = client.get(
        "/knowledge_panel?facet_name=packaging&facet_value=plastic-box&country=Germany"
    )
    assert response.status_code == 200
    assert response.json()
