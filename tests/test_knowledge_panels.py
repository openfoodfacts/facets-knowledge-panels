from app.main import hunger_game_kp, data_quality_kp
import requests
import app.main


def test_hunger_game_kp_with_filter_value_and_country():
    assert hunger_game_kp(
        hunger_game_filter="country", value="germany", country="france"
    ) == {
        "hunger-game": {
            "elements": [
                {
                    "element_type": "text",
                    "text_element": {
                        "html": "<p><a href='https://hunger.openfoodfacts.org/questions?country=germany'>Answer robotoff questions about germany</a></p>\n"
                    },
                }
            ]
        }
    }


def test_hunger_game_kp_with_category():
    assert hunger_game_kp(hunger_game_filter="category") == {
        "hunger-game": {
            "elements": [
                {
                    "element_type": "text",
                    "text_element": {
                        "html": "<p><a href='https://hunger.openfoodfacts.org/questions?type=category'>Answer robotoff questions about category</a></p>\n"
                    },
                }
            ]
        }
    }


def test_hunger_game_kp_category_with_country():
    assert hunger_game_kp(hunger_game_filter="category", country="france") == {
        "hunger-game": {
            "elements": [
                {
                    "element_type": "text",
                    "text_element": {
                        "html": "<p><a href='https://hunger.openfoodfacts.org/questions?country=france&type=category'>Answer robotoff questions about category</a></p>\n"
                    },
                }
            ]
        }
    }


def test_hunger_game_kp_category_with_value():
    assert hunger_game_kp(hunger_game_filter="category", value="beer") == {
        "hunger-game": {
            "elements": [
                {
                    "element_type": "text",
                    "text_element": {
                        "html": "<p><a href='https://hunger.openfoodfacts.org/questions?type=category&value_tag=beer'>Answer robotoff questions about beer category</a></p>\n"
                    },
                }
            ]
        }
    }


def test_hunger_game_kp_brand_with_value():
    assert hunger_game_kp(hunger_game_filter="brand", value="nestle") == {
        "hunger-game": {
            "elements": [
                {
                    "element_type": "text",
                    "text_element": {
                        "html": "<p><a href='https://hunger.openfoodfacts.org/questions?type=brand&value_tag=nestle'>Answer robotoff questions about nestle brand</a></p>\n"
                    },
                }
            ]
        }
    }


def test_hunger_game_kp_label_with_value():
    assert hunger_game_kp(hunger_game_filter="label", value="organic") == {
        "hunger-game": {
            "elements": [
                {
                    "element_type": "text",
                    "text_element": {
                        "html": "<p><a href='https://hunger.openfoodfacts.org/questions?type=label&value_tag=organic'>Answer robotoff questions about organic label</a></p>\n"
                    },
                }
            ]
        }
    }


def test_data_quality_kp_country_only(monkeypatch):
    class MockResponse(object):
        def __init__(self):
            self.url = "https://tr-en.openfoodfacts.org/data-quality.json"

        def json(self):
            return {
                "count": 125,
                "tags": [
                    {
                        "id": "en:ecoscore-production-system-no-label",
                        "known": 0,
                        "name": "ecoscore-production-system-no-label",
                        "products": 1393,
                        "url": "https://tr-en.openfoodfacts.org/data-quality/ecoscore-production-system-no-label",
                    },
                    {
                        "id": "en:no-packaging-data",
                        "known": 0,
                        "name": "no-packaging-data",
                        "products": 1345,
                        "url": "https://tr-en.openfoodfacts.org/data-quality/no-packaging-data",
                    },
                    {
                        "id": "en:ecoscore-packaging-packaging-data-missing",
                        "known": 0,
                        "name": "ecoscore-packaging-packaging-data-missing",
                        "products": 1328,
                        "url": "https://tr-en.openfoodfacts.org/data-quality/ecoscore-packaging-packaging-data-missing",
                    },
                ],
            }

    def mock_get(quality_url):
        return MockResponse()

    monkeypatch.setattr(requests, "get", mock_get)
    result = app.main.data_quality_kp(
        facet="country", value="Turkey", country="Hungary"
    )

    assert result == {
        "data-quality": {
            "elements": [
                {
                    "element_type": "text",
                    "total_issues": 125,
                    "text_element": '<ul><li><a href="https://tr-en.openfoodfacts.org/data-quality/ecoscore-production-system-no-label">1393 products with ecoscore-production-system-no-label</a></li>\n<li><a href="https://tr-en.openfoodfacts.org/data-quality/no-packaging-data">1345 products with no-packaging-data</a></li>\n<li><a href="https://tr-en.openfoodfacts.org/data-quality/ecoscore-packaging-packaging-data-missing">1328 products with ecoscore-packaging-packaging-data-missing</a></li></ul>',
                }
            ],
            "source_url": "https://tr-en.openfoodfacts.org/data-quality",
            "description": "This is a data-quality issues related to Turkey",
        }
    }


def test_data_quality_kp_with_facet_value_and_country(monkeypatch):
    class MockResponse(object):
        def __init__(self):
            self.url = (
                "https://hu-en.openfoodfacts.org/packaging/plastic-box/data-quality"
            )

        def json(self):
            return {"count": 0, "tags": []}

    def mock_get(quality_url):
        return MockResponse()

    monkeypatch.setattr(requests, "get", mock_get)
    result = app.main.data_quality_kp(
        facet="packaging", value="plastic-box", country="Hungary"
    )

    assert result == {
        "data-quality": {
            "elements": [
                {
                    "element_type": "text",
                    "total_issues": 0,
                    "text_element": "<ul></ul>",
                }
            ],
            "source_url": "https://hu-en.openfoodfacts.org/packaging/plastic-box/data-quality",
            "description": "This is a data-quality issues related to packaging based for Hungary",
        }
    }
