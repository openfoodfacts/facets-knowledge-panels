from app.main import hunger_game_kp
import requests
import app.main
from .test_utils import mock_get_factory
from app.off import tidy_html


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


def test_data_quality_kp_with_country(monkeypatch):
    expected_url = "https://tr-en.openfoodfacts.org/data-quality.json"
    expected_json = {
        "count": 125,
        "tags": [
            {
                "id": "en:ecoscore-production-system-no-label",
                "known": 0,
                "name": "ecoscore-production-system-no-label",
                "products": 1396,
                "url": "https://tr-en.openfoodfacts.org/data-quality/ecoscore-production-system-no-label",
            },
            {
                "id": "en:no-packaging-data",
                "known": 0,
                "name": "no-packaging-data",
                "products": 1348,
                "url": "https://tr-en.openfoodfacts.org/data-quality/no-packaging-data",
            },
            {
                "id": "en:ecoscore-packaging-packaging-data-missing",
                "known": 0,
                "name": "ecoscore-packaging-packaging-data-missing",
                "products": 1331,
                "url": "https://tr-en.openfoodfacts.org/data-quality/ecoscore-packaging-packaging-data-missing",
            },
        ],
    }
    monkeypatch.setattr(requests, "get", mock_get_factory(expected_url, expected_json))
    result = app.main.data_quality_kp(
        facet="country", value="Turkey", country="Hungary"
    )
    first_element = result["Quality"]["elements"][0]
    expected_text = """
    <p>The total number of issues are 125,here couples of issues</p>
    <ul>
        <li>
            <a href="https://tr-en.openfoodfacts.org/data-quality/ecoscore-production-system-no-label">1396 products with ecoscore-production-system-no-label</a>
        </li>
        <li>
            <a href="https://tr-en.openfoodfacts.org/data-quality/no-packaging-data">1348 products with no-packaging-data</a>
        </li>
        <li>
            <a href="https://tr-en.openfoodfacts.org/data-quality/ecoscore-packaging-packaging-data-missing">1331 products with ecoscore-packaging-packaging-data-missing</a>
        </li>
    </ul>
    """
    first_element["text_element"] = tidy_html(expected_text)

    assert result == {
        "Quality": {
            "title": "Data-quality issues",
            "subtitle": "Data-quality issues related to Turkey",
            "source_url": "https://tr-en.openfoodfacts.org/data-quality",
            "elements": [
                {
                    "element_type": "text",
                    "text_element": first_element["text_element"],
                }
            ],
        }
    }


def test_data_quality_kp_with_all_three_values(monkeypatch):
    expected_url = "https://world.openfoodfacts.org/brand/lidl/data-quality.json"
    expected_json = {
        "count": 173,
        "tags": [
            {
                "id": "en:ecoscore-origins-of-ingredients-origins-are-100-percent-unknown",
                "known": 0,
                "name": "ecoscore-origins-of-ingredients-origins-are-100-percent-unknown",
                "products": 6473,
                "url": "https://world.openfoodfacts.org/brand/lidl/data-quality/ecoscore-origins-of-ingredients-origins-are-100-percent-unknown",
            },
            {
                "id": "en:ecoscore-production-system-no-label",
                "known": 0,
                "name": "ecoscore-production-system-no-label",
                "products": 6467,
                "url": "https://world.openfoodfacts.org/brand/lidl/data-quality/ecoscore-production-system-no-label",
            },
            {
                "id": "en:no-packaging-data",
                "known": 0,
                "name": "no-packaging-data",
                "products": 5041,
                "url": "https://world.openfoodfacts.org/brand/lidl/data-quality/no-packaging-data",
            },
        ],
    }
    monkeypatch.setattr(requests, "get", mock_get_factory(expected_url, expected_json))
    result = app.main.data_quality_kp(facet="brand", value="lidl")
    first_element = result["Quality"]["elements"][0]
    expected_text = """ 
    <p>The total number of issues are 173,here couples of issues</p>
    <ul>
        <li>
            <a href="https://world.openfoodfacts.org/brand/lidl/data-quality/ecoscore-origins-of-ingredients-origins-are-100-percent-unknown">6473 products with ecoscore-origins-of-ingredients-origins-are-100-percent-unknown</a>
        </li>
        <li>
            <a href="https://world.openfoodfacts.org/brand/lidl/data-quality/ecoscore-production-system-no-label">6467 products with ecoscore-production-system-no-label</a>
        </li>
        <li>
            <a href="https://world.openfoodfacts.org/brand/lidl/data-quality/no-packaging-data">5041 products with no-packaging-data</a>
        </li>
    </ul>
    """
    first_element["text_element"] = tidy_html(expected_text)

    assert result == {
        "Quality": {
            "title": "Data-quality issues",
            "subtitle": "Data-quality issues related to brand lidl",
            "source_url": "https://world.openfoodfacts.org/brand/lidl/data-quality",
            "elements": [
                {
                    "element_type": "text",
                    "text_element": first_element["text_element"],
                }
            ],
        }
    }
