from curses import panel
from urllib import response
import json

from app.main import app, knowledge_panel
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
    response_body = response.json()
    assert response_body["knowledge_panels"] == []


def test_knowledge_panel_badendpoint():
    response = client.get("/knowledge_panel_bad")
    assert response.status_code == 404


def test_knowledge_panel_ctegory_with_value_and_country():
    assert knowledge_panel(
        facet_name="category", facet_value="chocolate", country="belgium"
    ) == {
        "knowledge_panels": [
            {
                "hunger-game": {
                    "elements": [
                        {
                            "element_type": "text",
                            "text_element": {
                                "html": "<p><a href='https://hunger.openfoodfacts.org/?country=belgium&type=category&value_tag=chocolate'>Answer robotoff questions about chocolate category</a></p>\n"
                            },
                        }
                    ]
                }
            }
        ]
    }


def test_knowledge_panel_ctegory_with_country():
    assert knowledge_panel(facet_name="category", country="india") == {
        "knowledge_panels": [
            {
                "hunger-game": {
                    "elements": [
                        {
                            "element_type": "text",
                            "text_element": {
                                "html": "<p><a href='https://hunger.openfoodfacts.org/?country=india&type=category'>Answer robotoff questions about category</a></p>\n"
                            },
                        }
                    ]
                }
            }
        ]
    }


def test_knowledge_panel_with_allergen():
    assert knowledge_panel(facet_name="allergen") == {"knowledge_panels": []}
