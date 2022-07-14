from curses import panel
from urllib import response

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
    response = client.get("/knowledge_panel")
    assert response.status_code == 422


def test_knowledge_panel_badendpoint():
    response = client.get("/knowledge_panel_bad")
    assert response.status_code == 404


def test_knowledge_panel_with_ctegory():
    assert knowledge_panel(facet_name="category") == {
        "knowledge_panels": [
            {
                "hunger-game": {
                    "elements": [
                        {
                            "element_type": "text",
                            "text_element": {
                                "html": "<p><a href='https://hunger.openfoodfacts.org/?type=category'></a></p>\n"
                            },
                        }
                    ]
                }
            }
        ]
    }


def test_knowledge_panel_ctegory_with_country():
    assert knowledge_panel(facet_name="category", country="India") == {
        "knowledge_panels": [
            {
                "hunger-game": {
                    "elements": [
                        {
                            "element_type": "text",
                            "text_element": {
                                "html": "<p><a href='https://hunger.openfoodfacts.org/?type=category&country=India'></a></p>\n"
                            },
                        }
                    ]
                }
            }
        ]
    }


def test_knowledge_panel_with_allergen():
    assert knowledge_panel(facet_name="allergen") == {"knowledge_panels": []}
