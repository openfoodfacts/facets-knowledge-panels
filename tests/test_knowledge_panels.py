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
    expected_url = "https://fr-en.openfoodfacts.org/api/v2/search"
    expected_json = {
        "count": 13552,
        "page": 1,
        "page_count": 24,
        "page_size": 24,
        "products": [
            {
                "code": "7624841856058",
                "last_edit_dates_tags": ["2022-07-27", "2022-07", "2022"],
                "last_editor": "gluten-scan",
                "product_name": "Red thai curry soup",
            },
            {
                "code": "8712566429271",
                "last_edit_dates_tags": ["2022-07-27", "2022-07", "2022"],
                "last_editor": "org-unilever-france-gms",
                "product_name": "Knorr Soupe Liquide Mouliné de Légumes d'Autrefois 1L",
            },
            {
                "code": "4023900542803",
                "last_edit_dates_tags": ["2022-07-26", "2022-07", "2022"],
                "last_editor": "prepperapp",
                "product_name": "Bio Soja Souce",
            },
        ],
    }
    monkeypatch.setattr(
        requests,
        "get",
        mock_get_factory(expected_url, expected_json),
    )
    result = app.main.last_edits_kp(facet="label", value="vegan", country="france")

    assert result == {
        "LastEdits": {
            "title": "Last-edites",
            "subtitle": "last-edits issues related to france label vegan",
            "source_url": "https://fr-en.openfoodfacts.org/label/vegan?sort_by=last_modified_t",
            "elements": [
                {
                    "element_type": "text",
                    "text_element": "<ul><p>Total number of edits 13552 </p>\n <li>Red thai curry soup (7624841856058) edited by gluten-scan on 2022-07-27</li>\n<li>Knorr Soupe Liquide Mouliné de Légumes d'Autrefois 1L (8712566429271) edited by org-unilever-france-gms on 2022-07-27</li>\n<li>Bio Soja Souce (4023900542803) edited by prepperapp on 2022-07-26</li>\n<li>Berry Revolutionary (8711327539303) edited by kiliweb on 2022-07-26</li>\n<li>Gelées con succhi Di frutta (8016042021011) edited by kiliweb on 2022-07-26</li>\n<li>Minifrühlingsrollen mit Gemüse (4316268371421) edited by blaerf on 2022-07-26</li>\n<li>Chicorée 0% Caffeine (5411788047166) edited by kiliweb on 2022-07-26</li>\n<li>Soy sauce (8715035110502) edited by frazerclews on 2022-07-26</li>\n<li>Sables pépites de chocolat (3760154260619) edited by kiliweb on 2022-07-26</li>\n<li>Raw pasta Fettuccine (8718868683878) edited by kiliweb on 2022-07-26</li></ul>",
                }
            ],
        }
    }
