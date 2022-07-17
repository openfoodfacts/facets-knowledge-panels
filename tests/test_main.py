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


def test_knowledge_panel_badendpoint():
    response = client.get("/knowledge_panel_bad")
    assert response.status_code == 404


def test_knowledge_panel_ctegory_with_value_and_country():
    assert knowledge_panel(
        facet_name="packaging", facet_value="plastic-box", country="italy"
    ) == {
        "knowledge_panels": [
            {
                "data-quality": {
                    "elements": [
                        {
                            "element_type": "text",
                            "total_issues": 0,
                            "text_element": [],
                            "source_url": "https://world.openfoodfacts.org/country/italy/packaging/plastic-box/data-quality.json",
                            "description": "data-quality issues related to packaging based for italy",
                        }
                    ]
                }
            }
        ]
    }


def test_knowledge_panel_ctegory_with_country():
    assert knowledge_panel(facet_name="origin", country="India") == {
        "knowledge_panels": [
            {
                "data-quality": {
                    "elements": [
                        {
                            "element_type": "text",
                            "total_issues": 0,
                            "text_element": [],
                            "source_url": "https://world.openfoodfacts.org/country/India/origin/None/data-quality.json",
                            "description": "data-quality issues related to origin based for India",
                        }
                    ]
                }
            }
        ]
    }


def test_knowledge_panel_with_allergen():
    assert knowledge_panel(facet_name="allergen") == {
        "knowledge_panels": [
            {
                "data-quality": {
                    "elements": [
                        {
                            "element_type": "text",
                            "total_issues": 171,
                            "text_element": [
                                {
                                    "id": "en:ingredients-percent-analysis-ok",
                                    "known": 0,
                                    "name": "ingredients-percent-analysis-ok",
                                    "products": 1308,
                                    "url": "https://world.openfoodfacts.org/allergen/none/data-quality/ingredients-percent-analysis-ok",
                                },
                                {
                                    "id": "en:ecoscore-production-system-no-label",
                                    "known": 0,
                                    "name": "ecoscore-production-system-no-label",
                                    "products": 1258,
                                    "url": "https://world.openfoodfacts.org/allergen/none/data-quality/ecoscore-production-system-no-label",
                                },
                                {
                                    "id": "en:ecoscore-origins-of-ingredients-origins-are-100-percent-unknown",
                                    "known": 0,
                                    "name": "ecoscore-origins-of-ingredients-origins-are-100-percent-unknown",
                                    "products": 1168,
                                    "url": "https://world.openfoodfacts.org/allergen/none/data-quality/ecoscore-origins-of-ingredients-origins-are-100-percent-unknown",
                                },
                            ],
                            "source_url": "https://world.openfoodfacts.org/allergen/None/data-quality.json",
                            "description": "data-quality issues related to allergen",
                        }
                    ]
                }
            }
        ]
    }
