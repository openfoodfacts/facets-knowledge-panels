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
        facet_name="category", facet_value="chocolates", country="belgium"
    ) == {
        "knowledge_panels": [
            {
                "hunger-game": {
                    "elements": [
                        {
                            "element_type": "text",
                            "text_element": {
                                "html": "<p><a href='https://hunger.openfoodfacts.org/questions?country=belgium&type=category&value_tag=chocolates'>Answer robotoff questions about chocolates category</a></p>\n"
                            },
                        }
                    ]
                }
            },
            {
                "last-edits": {
                    "elements": [
                        {
                            "element_type": "text",
                            "total_issues": 17028,
                            "text_element": [
                                {"code": "3664346305860", "last_editor": "jul45"},
                                {
                                    "code": "5201127034724",
                                    "last_editor": "ayyyvocado",
                                    "product_name": "Ион Дарк Шок. 72 % Какао и Цели Бадеми",
                                },
                                {
                                    "code": "3560071265564",
                                    "last_editor": "kiliweb",
                                    "product_name": "Chocolat noir noisettes entières",
                                },
                            ],
                            "source_url": "https://world.openfoodfacts.org/api/v2/search?categories_tags_en=chocolates&fields=code%2Cproduct_name%2Clast_editor&sort_by=last_modified_t",
                        }
                    ]
                }
            },
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
                                "html": "<p><a href='https://hunger.openfoodfacts.org/questions?country=india&type=category'>Answer robotoff questions about category</a></p>\n"
                            },
                        }
                    ]
                }
            }
        ]
    }


def test_knowledge_panel_with_allergen():
    assert knowledge_panel(facet_name="allergen") == {"knowledge_panels": []}
