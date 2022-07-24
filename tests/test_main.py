import app.main
from curses import panel
from urllib import response
import json
import requests
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


def test_knowledge_panel_country_only(monkeypatch):
    class MockResponse(object):
        def __init__(self):
            self.url = "https://au.openfoodfacts.org/data-quality.json"

        def json(self):
            return {
                "count": 173,
                "tags": [
                    {
                        "id": "en:ecoscore-production-system-no-label",
                        "known": 0,
                        "name": "ecoscore-production-system-no-label",
                        "products": 25222,
                        "url": "https://au.openfoodfacts.org/data-quality/ecoscore-production-system-no-label",
                    },
                    {
                        "id": "en:ecoscore-origins-of-ingredients-origins-are-100-percent-unknown",
                        "known": 0,
                        "name": "ecoscore-origins-of-ingredients-origins-are-100-percent-unknown",
                        "products": 23731,
                        "url": "https://au.openfoodfacts.org/data-quality/ecoscore-origins-of-ingredients-origins-are-100-percent-unknown",
                    },
                    {
                        "id": "en:no-packaging-data",
                        "known": 0,
                        "name": "no-packaging-data",
                        "products": 22649,
                        "url": "https://au.openfoodfacts.org/data-quality/no-packaging-data",
                    },
                    {
                        "id": "en:ecoscore-packaging-packaging-data-missing",
                        "known": 0,
                        "name": "ecoscore-packaging-packaging-data-missing",
                        "products": 22437,
                        "url": "https://au.openfoodfacts.org/data-quality/ecoscore-packaging-packaging-data-missing",
                    },
                ],
            }

    def mock_get(quality_url):
        return MockResponse()

    monkeypatch.setattr(requests, "get", mock_get)
    result = knowledge_panel(
        facet_name="country", facet_value="Australia", country="Canada"
    )

    assert result == {
        "knowledge_panels": [
            {
                "hunger-game": {
                    "elements": [
                        {
                            "element_type": "text",
                            "text_element": {
                                "html": "<p><a href='https://hunger.openfoodfacts.org/questions?country=Australia'>Answer robotoff questions about Australia</a></p>\n"
                            },
                        }
                    ]
                }
            },
            {
                "data-quality": {
                    "elements": [
                        {
                            "element_type": "text",
                            "total_issues": 173,
                            "text_element": '<ul><li><a href="https://au.openfoodfacts.org/data-quality/ecoscore-production-system-no-label">25222 products with ecoscore-production-system-no-label</a></li>\n<li><a href="https://au.openfoodfacts.org/data-quality/ecoscore-origins-of-ingredients-origins-are-100-percent-unknown">23731 products with ecoscore-origins-of-ingredients-origins-are-100-percent-unknown</a></li>\n<li><a href="https://au.openfoodfacts.org/data-quality/no-packaging-data">22649 products with no-packaging-data</a></li></ul>',
                        }
                    ],
                    "source_url": "https://au-en.openfoodfacts.org/data-quality",
                    "description": "This is a data-quality issues related to Australia",
                }
            },
        ]
    }


def test_knowledge_panel_facet_value_and_country(monkeypatch):
    class MockResponse(object):
        def __init__(self):
            self.url = "https://at-en.openfoodfacts.org/allergen/nuts/data-quality.json"

        def json(self):
            return {
                "count": 96,
                "tags": [
                    {
                        "id": "en:ecoscore-origins-of-ingredients-origins-are-100-percent-unknown",
                        "known": 0,
                        "name": "ecoscore-origins-of-ingredients-origins-are-100-percent-unknown",
                        "products": 316,
                        "url": "https://at-en.openfoodfacts.org/allergen/nuts/data-quality/ecoscore-origins-of-ingredients-origins-are-100-percent-unknown",
                    },
                    {
                        "id": "en:ingredients-percent-analysis-ok",
                        "known": 0,
                        "name": "ingredients-percent-analysis-ok",
                        "products": 276,
                        "url": "https://at-en.openfoodfacts.org/allergen/nuts/data-quality/ingredients-percent-analysis-ok",
                    },
                    {
                        "id": "en:ecoscore-production-system-no-label",
                        "known": 0,
                        "name": "ecoscore-production-system-no-label",
                        "products": 274,
                        "url": "https://at-en.openfoodfacts.org/allergen/nuts/data-quality/ecoscore-production-system-no-label",
                    },
                ],
            }

    def mock_get(quality_url):
        return MockResponse()

    monkeypatch.setattr(requests, "get", mock_get)
    result = knowledge_panel(
        facet_name="allergen", facet_value="nuts", country="Austria"
    )

    assert result == {
        "knowledge_panels": [
            {
                "data-quality": {
                    "elements": [
                        {
                            "element_type": "text",
                            "total_issues": 96,
                            "text_element": '<ul><li><a href="https://at-en.openfoodfacts.org/allergen/nuts/data-quality/ecoscore-origins-of-ingredients-origins-are-100-percent-unknown">316 products with ecoscore-origins-of-ingredients-origins-are-100-percent-unknown</a></li>\n<li><a href="https://at-en.openfoodfacts.org/allergen/nuts/data-quality/ingredients-percent-analysis-ok">276 products with ingredients-percent-analysis-ok</a></li>\n<li><a href="https://at-en.openfoodfacts.org/allergen/nuts/data-quality/ecoscore-production-system-no-label">274 products with ecoscore-production-system-no-label</a></li></ul>',
                        }
                    ],
                    "source_url": "https://at-en.openfoodfacts.org/allergen/nuts/data-quality",
                    "description": "This is a data-quality issues related to allergen based for Austria",
                }
            }
        ]
    }
