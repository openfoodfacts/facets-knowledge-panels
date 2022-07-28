from ast import Param
from app.main import hunger_game_kp, last_edits_kp
import requests
import app.main
from .test_utils import mock_get_factory


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


def test_last_edits_kp_with_all_three_values(monkeypatch):
    expected_url = "https://hu-en.openfoodfacts.org/api/v2/search"
    expected_kwargs = {
        "params": {
            "fields": "product_name,code,last_editor,last_edit_dates_tags",
            "sort_by": "last_modified_t",
            "vitamins_tags_en": "vitamin-k",
        }
    }
    expected_json = {
        "count": 1,
        "page": 1,
        "page_count": 1,
        "page_size": 24,
        "products": [
            {
                "code": "0715235567418",
                "last_edit_dates_tags": ["2022-02-10", "2022-02", "2022"],
                "last_editor": "packbot",
                "product_name": "Tiqle Sticks Strawberry taste",
            }
        ],
    }
    monkeypatch.setattr(
        requests,
        "get",
        mock_get_factory(
            expected_url,
            expected_kwargs,
            expected_json,
        ),
    )
    result = app.main.last_edits_kp(
        facet="vitamin", value="vitamin-k", country="hungary"
    )

    assert result == {
        "LastEdits": {
            "title": "Last-edites",
            "subtitle": "last-edits issues related to hungary vitamin vitamin-k",
            "source_url": "https://hu-en.openfoodfacts.org/vitamin/vitamin-k?sort_by=last_modified_t",
            "elements": [
                {
                    "element_type": "text",
                    "text_element": "<ul><p>Total number of edits 1 </p>\n <li>Tiqle Sticks Strawberry taste (0715235567418) edited by packbot on 2022-02-10</li></ul>",
                }
            ],
        }
    }
