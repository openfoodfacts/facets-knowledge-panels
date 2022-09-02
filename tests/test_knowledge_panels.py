import requests
import wikidata.client

import app.main
from app.i18n import active_translation
from app.main import hunger_game_kp
from app.wikidata_utils import wikidata_props

from .test_utils import DictAttr, mock_get_factory, mock_wikidata_get, tidy_html


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
    json_content = {
        "count": 125,
        "tags": [
            {
                "id": "en:ecoscore-production-system-no-label",
                "known": 0,
                "name": "ecoscore-production-system-no-label",
                "products": 1583,
                "url": "https://tr-en.openfoodfacts.org/data-quality/ecoscore-production-system-no-label",
            },
            {
                "id": "en:no-packaging-data",
                "known": 0,
                "name": "no-packaging-data",
                "products": 1531,
                "url": "https://tr-en.openfoodfacts.org/data-quality/no-packaging-data",
            },
            {
                "id": "en:ecoscore-origins-of-ingredients-origins-are-100-percent-unknown",
                "known": 0,
                "name": "ecoscore-origins-of-ingredients-origins-are-100-percent-unknown",
                "products": 1515,
                "url": "https://tr-en.openfoodfacts.org/data-quality/ecoscore-origins-of-ingredients-origins-are-100-percent-unknown",
            },
        ],
    }

    monkeypatch.setattr(
        requests, "get", mock_get_factory(expected_url, json_content=json_content)
    )
    result = app.main.data_quality_kp(
        facet="country", value="Turkey", country="Hungary"
    )
    first_element = result["Quality"]["elements"][0]
    first_element["text_element"] = tidy_html(first_element["text_element"])
    expected_text = """
    <ul>
        <p>The total number of issues are 125</p>
        <li>
            <a herf=https://tr-en.openfoodfacts.org/data-quality/ecoscore-production-system-no-label>1583 products with ecoscore-production-system-no-label</a>
        </li>
        <li>
            <a herf=https://tr-en.openfoodfacts.org/data-quality/no-packaging-data>1531 products with no-packaging-data</a>
        </li>
        <li>
            <a herf=https://tr-en.openfoodfacts.org/data-quality/ecoscore-origins-of-ingredients-origins-are-100-percent-unknown>1515 products with ecoscore-origins-of-ingredients-origins-are-100-percent-unknown</a>
        </li>
    </ul>
    """
    # assert html separately to have better output in case of error
    assert first_element["text_element"] == tidy_html(expected_text)
    # now replace it for concision of output
    first_element["text_element"] = "ok"
    assert result == {
        "Quality": {
            "title": "Data-quality issues",
            "subtitle": "Data-quality issues related to Turkey ",
            "source_url": "https://tr-en.openfoodfacts.org/data-quality",
            "elements": [
                {
                    "element_type": "text",
                    "text_element": "ok",
                }
            ],
        }
    }


def test_data_quality_kp_with_all_three_values(monkeypatch):
    expected_url = "https://world.openfoodfacts.org/brand/lidl/data-quality.json"
    json_content = {
        "count": 182,
        "tags": [
            {
                "id": "en:ecoscore-origins-of-ingredients-origins-are-100-percent-unknown",
                "known": 0,
                "name": "ecoscore-origins-of-ingredients-origins-are-100-percent-unknown",
                "products": 7688,
                "url": "https://world.openfoodfacts.org/brand/lidl/data-quality/ecoscore-origins-of-ingredients-origins-are-100-percent-unknown",
            },
            {
                "id": "en:ecoscore-production-system-no-label",
                "known": 0,
                "name": "ecoscore-production-system-no-label",
                "products": 7661,
                "url": "https://world.openfoodfacts.org/brand/lidl/data-quality/ecoscore-production-system-no-label",
            },
            {
                "id": "en:no-packaging-data",
                "known": 0,
                "name": "no-packaging-data",
                "products": 6209,
                "url": "https://world.openfoodfacts.org/brand/lidl/data-quality/no-packaging-data",
            },
        ],
    }

    monkeypatch.setattr(
        requests, "get", mock_get_factory(expected_url, json_content=json_content)
    )
    result = app.main.data_quality_kp(facet="brand", value="lidl")
    first_element = result["Quality"]["elements"][0]
    first_element["text_element"] = tidy_html(first_element["text_element"])
    expected_text = """
    <ul>
        <p>The total number of issues are 182</p>
        <li>
            <a herf=https://world.openfoodfacts.org/brand/lidl/data-quality/ecoscore-origins-of-ingredients-origins-are-100-percent-unknown>7688 products with ecoscore-origins-of-ingredients-origins-are-100-percent-unknown</a>
        </li>
        <li>
            <a herf=https://world.openfoodfacts.org/brand/lidl/data-quality/ecoscore-production-system-no-label>7661 products with ecoscore-production-system-no-label</a>
        </li>
        <li>
            <a herf=https://world.openfoodfacts.org/brand/lidl/data-quality/no-packaging-data>6209 products with no-packaging-data</a>
        </li>
    </ul>
    """
    # assert html separately to have better output in case of error
    assert first_element["text_element"] == tidy_html(expected_text)
    # now replace it for concision of output
    first_element["text_element"] = "ok"
    assert result == {
        "Quality": {
            "title": "Data-quality issues",
            "subtitle": "Data-quality issues related to brand lidl",
            "source_url": "https://world.openfoodfacts.org/brand/lidl/data-quality",
            "elements": [
                {
                    "element_type": "text",
                    "text_element": "ok",
                }
            ],
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
    json_content = {
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
            json_content,
        ),
    )
    result = app.main.last_edits_kp(
        facet="vitamin", value="vitamin-k", country="hungary"
    )
    first_element = result["LastEdits"]["elements"][0]
    first_element["text_element"] = tidy_html(first_element["text_element"])
    last_edits_text = """
    <ul>
        <p>Total number of edits 1 </p>
        <li>
            Tiqle Sticks Strawberry taste (0715235567418) edited by packbot on 2022-02-10
        </li>
    </ul>
    """
    # assert html separately to have better output in case of error
    assert first_element["text_element"] == tidy_html(last_edits_text)
    # now replace it for concision of output
    first_element["text_element"] = "ok"
    assert result == {
        "LastEdits": {
            "title": "Last-edits",
            "subtitle": "last-edits issues related to hungary vitamin vitamin-k",
            "source_url": "https://hu-en.openfoodfacts.org/vitamin/vitamin-k?sort_by=last_modified_t",
            "elements": [
                {
                    "element_type": "text",
                    "text_element": "ok",
                }
            ],
        }
    }


def test_wikidata_kp(monkeypatch):
    # first mock the call to open food facts (to get the wikidata property)
    expected_url = "https://world.openfoodfacts.org/api/v2/taxonomy"
    expected_kwargs = {
        "params": {
            "tagtype": "categories",
            "fields": "wikidata",
            "tags": "fr:fitou",
        }
    }
    json_content = {"fr:fitou": {"parents": [], "wikidata": {"en": "Q470974"}}}
    monkeypatch.setattr(
        requests,
        "get",
        mock_get_factory(
            expected_url,
            expected_kwargs,
            json_content,
        ),
    )
    # then mock the call to wikidata
    # fake entity mimicks the Entity object from wikidata library
    fake_entity = {
        "description": {"en": "French wine appellation"},
        "label": {"en": "Fitou AOC"},
        wikidata_props.image_prop: DictAttr(
            image_url="https://upload.wikimedia.org/wikipedia/commons/d/d6/Paziols_%28France%29_Vue_du_village.jpg"
        ),
        wikidata_props.OSM_prop: "2727716",
        wikidata_props.INAO_prop: "6159",
        "attributes": {
            "sitelinks": {"enwiki": {"a": "http://en.wikipedia.org/wiki/Fitou_AOC"}}
        },
    }
    monkeypatch.setattr(
        wikidata.client.Client,
        "get",
        mock_wikidata_get("Q470974", fake_entity),
    )
    # run the test
    result = app.main.wikidata_kp(facet="category", value="fr:fitou")
    expected_result = {
        "WikiData": {
            "title": "wiki-data",
            "subtitle": "French wine appellation",
            "source_url": "https://www.wikidata.org/wiki/Q470974",
            "elements": [
                {
                    "element_type": "text",
                    "text_element": "Fitou AOC",
                    "image_url": "https://upload.wikimedia.org/wikipedia/commons/d/d6/Paziols_%28France%29_Vue_du_village.jpg",
                },
                {
                    "element_type": "links",
                    "wikipedia": "http://en.wikipedia.org/wiki/Fitou_AOC",
                    "open_street_map": "https://www.openstreetmap.org/relation/2727716",
                    "INAO": "https://www.inao.gouv.fr/produit/6159",
                },
            ],
        }
    }
    assert result == expected_result
