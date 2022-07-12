import requests
from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_hello():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Hello from facets-knowledge-panels! Tip: open /docs for documentation"}


def test_knowledge_panel_hunger_game():
    response = client.get("/hunger-game-kp")
    assert response.status_code == 422
    return response.json()
