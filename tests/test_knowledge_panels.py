import pytest
import requests
import wikidata.client

import app.main
from app.i18n import active_translation
from app.main import hunger_game_kp
from app.wikidata_utils import wikidata_props

from .test_utils import DictAttr, mock_get_factory, mock_wikidata_get, tidy_html


@pytest.fixture(autouse=True)
def auto_activate_lang():
    """auto activate translations for each function"""
    with active_translation():
        yield


def test_hunger_game_kp_with_filter_value_and_country():
    html = (
        "<p><a href='https://hunger.openfoodfacts.org/questions?country=germany'>"
        "Answer robotoff questions about germany</a></p>\n"
    )
    assert hunger_game_kp(hunger_game_filter="country", value="germany", country="france") == {
        "hunger-game": {
            "elements": [
                {
                    "element_type": "text",
                    "text_element": {
                        "html": html,
                    },
                }
            ]
        }
    }


def test_hunger_game_kp_with_category():
    html = (
        "<p><a href='https://hunger.openfoodfacts.org/questions?type=category'>"
        "Answer robotoff questions about category</a></p>\n"
    )
    assert hunger_game_kp(hunger_game_filter="category") == {
        "hunger-game": {
            "elements": [
                {
                    "element_type": "text",
                    "text_element": {
                        "html": html,
                    },
                }
            ]
        }
    }


def test_hunger_game_kp_category_with_country():
    html = (
        "<p><a href='https://hunger.openfoodfacts.org/questions?country=france&type=category'>"
        "Answer robotoff questions about category</a></p>\n"
    )
    assert hunger_game_kp(hunger_game_filter="category", country="france") == {
        "hunger-game": {
            "elements": [
                {
                    "element_type": "text",
                    "text_element": {
                        "html": html,
                    },
                }
            ]
        }
    }


def test_hunger_game_kp_category_with_value():
    html = (
        "<p><a href='https://hunger.openfoodfacts.org/questions?type=category&value_tag=beer'>"
        "Answer robotoff questions about beer category</a></p>\n"
    )
    assert hunger_game_kp(hunger_game_filter="category", value="beer") == {
        "hunger-game": {
            "elements": [
                {
                    "element_type": "text",
                    "text_element": {
                        "html": html,
                    },
                }
            ]
        }
    }


def test_hunger_game_kp_brand_with_value():
    html = (
        "<p><a href='https://hunger.openfoodfacts.org/questions?type=brand&value_tag=nestle'>"
        "Answer robotoff questions about nestle brand</a></p>\n"
    )
    assert hunger_game_kp(hunger_game_filter="brand", value="nestle") == {
        "hunger-game": {
            "elements": [
                {
                    "element_type": "text",
                    "text_element": {
                        "html": html,
                    },
                }
            ]
        }
    }


def test_hunger_game_kp_label_with_value():
    html = (
        "<p><a href='https://hunger.openfoodfacts.org/questions?type=label&value_tag=organic'>"
        "Answer robotoff questions about organic label</a></p>\n"
    )
    assert hunger_game_kp(hunger_game_filter="label", value="organic") == {
        "hunger-game": {
            "elements": [
                {
                    "element_type": "text",
                    "text_element": {
                        "html": html,
                    },
                }
            ]
        }
    }


def test_data_quality_kp_with_country(monkeypatch):
    expected_url = "https://tr-en.openfoodfacts.org/data-quality.json"
    base_url = "https://tr-en.openfoodfacts.org/data-quality"
    json_content = {
        "count": 125,
        "tags": [
            {
                "id": "en:ecoscore-production-system-no-label",
                "known": 0,
                "name": "ecoscore-production-system-no-label",
                "products": 1583,
                "url": f"{base_url}/ecoscore-production-system-no-label",
            },
            {
                "id": "en:no-packaging-data",
                "known": 0,
                "name": "no-packaging-data",
                "products": 1531,
                "url": f"{base_url}/no-packaging-data",
            },
            {
                "id": "en:ecoscore-origins-of-ingredients-origins-are-100-percent-unknown",
                "known": 0,
                "name": "ecoscore-origins-of-ingredients-origins-are-100-percent-unknown",
                "products": 1515,
                "url": (
                    f"{base_url}/" "ecoscore-origins-of-ingredients-origins-are-100-percent-unknown"
                ),
            },
        ],
    }

    monkeypatch.setattr(requests, "get", mock_get_factory(expected_url, json_content=json_content))
    result = app.main.data_quality_kp(facet="country", value="Turkey", country="Hungary")
    first_element = result["Quality"]["elements"][0]
    first_element["text_element"] = tidy_html(first_element["text_element"])
    expected_text = """
    <ul>
        <p>The total number of issues are 125</p>
        <li>
            <a href=https://tr-en.openfoodfacts.org/data-quality/ecoscore-production-system-no-label>1583 products with ecoscore-production-system-no-label</a>
        </li>
        <li>
            <a href=https://tr-en.openfoodfacts.org/data-quality/no-packaging-data>1531 products with no-packaging-data</a>
        </li>
        <li>
            <a href=https://tr-en.openfoodfacts.org/data-quality/ecoscore-origins-of-ingredients-origins-are-100-percent-unknown>1515 products with ecoscore-origins-of-ingredients-origins-are-100-percent-unknown</a>
        </li>
    </ul>
    """  # noqa: E501  # allow long lines
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


def test_data_quality_kp_with_one_facet_and_value(monkeypatch):
    expected_url = "https://world.openfoodfacts.org/brand/lidl/data-quality.json"
    base_url = "https://world.openfoodfacts.org/brand/lidl/data-quality"
    json_content = {
        "count": 182,
        "tags": [
            {
                "id": "en:ecoscore-origins-of-ingredients-origins-are-100-percent-unknown",
                "known": 0,
                "name": "ecoscore-origins-of-ingredients-origins-are-100-percent-unknown",
                "products": 7688,
                "url": (
                    f"{base_url}/" "ecoscore-origins-of-ingredients-origins-are-100-percent-unknown"
                ),
            },
            {
                "id": "en:ecoscore-production-system-no-label",
                "known": 0,
                "name": "ecoscore-production-system-no-label",
                "products": 7661,
                "url": f"{base_url}/ecoscore-production-system-no-label",
            },
            {
                "id": "en:no-packaging-data",
                "known": 0,
                "name": "no-packaging-data",
                "products": 6209,
                "url": f"{base_url}/no-packaging-data",
            },
        ],
    }

    monkeypatch.setattr(requests, "get", mock_get_factory(expected_url, json_content=json_content))
    result = app.main.data_quality_kp(facet="brand", value="lidl")
    first_element = result["Quality"]["elements"][0]
    first_element["text_element"] = tidy_html(first_element["text_element"])
    expected_text = """
    <ul>
        <p>The total number of issues are 182</p>
        <li>
            <a href=https://world.openfoodfacts.org/brand/lidl/data-quality/ecoscore-origins-of-ingredients-origins-are-100-percent-unknown>7688 products with ecoscore-origins-of-ingredients-origins-are-100-percent-unknown</a>
        </li>
        <li>
            <a href=https://world.openfoodfacts.org/brand/lidl/data-quality/ecoscore-production-system-no-label>7661 products with ecoscore-production-system-no-label</a>
        </li>
        <li>
            <a href=https://world.openfoodfacts.org/brand/lidl/data-quality/no-packaging-data>6209 products with no-packaging-data</a>
        </li>
    </ul>
    """  # noqa: E501  # allow long lines
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


def test_data_quality_kp_with_all_tags(monkeypatch):
    expected_url = (
        "https://world.openfoodfacts.org/category/beers/brand/budweiser/data-quality.json"
    )
    json_content = {
        "count": 24,
        "tags": [
            {
                "id": "en:alcoholic-beverages-category-without-alcohol-value",
                "known": 0,
                "name": "alcoholic-beverages-category-without-alcohol-value",
                "products": 13,
                "url": "https://world.openfoodfacts.org/category/beers/data-quality/alcoholic-beverages-category-without-alcohol-value",
            },
            {
                "id": "en:ecoscore-production-system-no-label",
                "known": 0,
                "name": "ecoscore-production-system-no-label",
                "products": 13,
                "url": "https://world.openfoodfacts.org/category/beers/data-quality/ecoscore-production-system-no-label",
            },
            {
                "id": "en:ecoscore-origins-of-ingredients-origins-are-100-percent-unknown",
                "known": 0,
                "name": "ecoscore-origins-of-ingredients-origins-are-100-percent-unknown",
                "products": 12,
                "url": "https://world.openfoodfacts.org/category/beers/data-quality/ecoscore-origins-of-ingredients-origins-are-100-percent-unknown",
            },
        ],
    }

    monkeypatch.setattr(requests, "get", mock_get_factory(expected_url, json_content=json_content))
    result = app.main.data_quality_kp(
        facet="category", value="beers", sec_facet="brand", sec_value="budweiser"
    )
    first_element = result["Quality"]["elements"][0]
    first_element["text_element"] = tidy_html(first_element["text_element"])
    expected_text = """
    <ul>
        <p>The total number of issues are 24</p>
        <li>
            <a herf=https://world.openfoodfacts.org/category/beers/data-quality/alcoholic-beverages-category-without-alcohol-value>13 products with alcoholic-beverages-category-without-alcohol-value</a>
        </li>
        <li>
            <a herf=https://world.openfoodfacts.org/category/beers/data-quality/ecoscore-production-system-no-label>13 products with ecoscore-production-system-no-label</a>
        </li>
        <li>
            <a herf=https://world.openfoodfacts.org/category/beers/data-quality/ecoscore-origins-of-ingredients-origins-are-100-percent-unknown>12 products with ecoscore-origins-of-ingredients-origins-are-100-percent-unknown</a>
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
            "subtitle": "Data-quality issues related to category beers brand budweiser",
            "source_url": "https://world.openfoodfacts.org/category/beers/brand/budweiser/data-quality",
            "elements": [
                {
                    "element_type": "text",
                    "text_element": "ok",
                }
            ],
        }
    }


def test_last_edits_kp_with_one_facet_and_value(monkeypatch):
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
    result = app.main.last_edits_kp(facet="vitamin", value="vitamin-k", country="hungary")
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
            "source_url": (
                "https://hu-en.openfoodfacts.org/vitamin/vitamin-k?sort_by=last_modified_t"
            ),
            "elements": [
                {
                    "element_type": "text",
                    "text_element": "ok",
                }
            ],
        }
    }


def test_last_edits_kp_with_all_tags(monkeypatch):
    expected_url = "https://fr-en.openfoodfacts.org/api/v2/search"
    expected_kwargs = {
        "params": {
            "fields": "product_name,code,last_editor,last_edit_dates_tags",
            "sort_by": "last_modified_t",
            "brands_tags_en": "nestle",
            "categories_tags_en": "coffees",
        }
    }
    json_content = {
        "count": 112,
        "page": 1,
        "page_count": 24,
        "page_size": 24,
        "products": [
            {
                "code": "7613036271868",
                "last_edit_dates_tags": ["2022-08-31", "2022-08", "2022"],
                "last_editor": "org-nestle-france",
                "product_name": "Capsules NESCAFE Dolce Gusto Cappuccino Extra Crema 16 Capsules",
            },
            {
                "code": "7613032655495",
                "last_edit_dates_tags": ["2022-08-30", "2022-08", "2022"],
                "last_editor": "feat",
                "product_name": "RICORE Original, Café & Chicorée, Boîte 260g",
            },
            {
                "code": "7613036303521",
                "last_edit_dates_tags": ["2022-08-28", "2022-08", "2022"],
                "last_editor": "feat",
                "product_name": "Ricoré",
            },
            {
                "code": "3033710072927",
                "last_edit_dates_tags": ["2022-08-28", "2022-08", "2022"],
                "last_editor": "org-nestle-france",
                "product_name": "NESCAFÉ NES, Café Soluble, Boîte de 25 Sticks (2g chacun)",
            },
            {
                "code": "3033710076017",
                "last_edit_dates_tags": ["2022-08-28", "2022-08", "2022"],
                "last_editor": "org-nestle-france",
                "product_name": "NESCAFÉ SPECIAL FILTRE L'Original, Café Soluble, Boîte de 25 Sticks",
            },
            {
                "code": "3033710074624",
                "last_edit_dates_tags": ["2022-08-28", "2022-08", "2022"],
                "last_editor": "org-nestle-france",
                "product_name": "NESCAFÉ SPECIAL FILTRE Décaféiné, Café Soluble, Flacon de 200g",
            },
            {
                "code": "7613034056122",
                "last_edit_dates_tags": ["2022-08-28", "2022-08", "2022"],
                "last_editor": "org-nestle-france",
                "product_name": "NESCAFÉ SPECIAL FILTRE L'Original, Café Soluble, Recharge de 150g",
            },
            {
                "code": "3033710074525",
                "last_edit_dates_tags": ["2022-08-28", "2022-08", "2022"],
                "last_editor": "org-nestle-france",
                "product_name": "NESCAFÉ SPECIAL FILTRE L'Original Flacon de 200g",
            },
            {
                "code": "3033710074518",
                "last_edit_dates_tags": ["2022-08-28", "2022-08", "2022"],
                "last_editor": "org-nestle-france",
            },
            {
                "code": "7891000300602",
                "last_edit_dates_tags": ["2022-08-27", "2022-08", "2022"],
                "last_editor": "5m4u9",
                "product_name": "Original",
            },
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
        facet="brand",
        value="nestle",
        sec_facet="category",
        sec_value="coffees",
        country="france",
    )
    first_element = result["LastEdits"]["elements"][0]
    first_element["text_element"] = tidy_html(first_element["text_element"])
    last_edits_text = """
    <ul>
        <p>Total number of edits 112</p>
        <li>
            Capsules NESCAFE Dolce Gusto Cappuccino Extra Crema 16 Capsules (7613036271868) edited by org-nestle-france on 2022-08-31
        </li>
        <li>
            RICORE Original, Café & Chicorée, Boîte 260g (7613032655495) edited by feat on 2022-08-30
        </li>
        <li>
            Ricoré (7613036303521) edited by feat on 2022-08-28
        </li>
        <li>
            NESCAFÉ NES, Café Soluble, Boîte de 25 Sticks (2g chacun) (3033710072927) edited by org-nestle-france on 2022-08-28
        </li>
        <li>
            NESCAFÉ SPECIAL FILTRE L'Original, Café Soluble, Boîte de 25 Sticks (3033710076017) edited by org-nestle-france on 2022-08-28
        </li>
        <li>
            NESCAFÉ SPECIAL FILTRE Décaféiné, Café Soluble, Flacon de 200g (3033710074624) edited by org-nestle-france on 2022-08-28
        </li>
        <li>
            NESCAFÉ SPECIAL FILTRE L'Original, Café Soluble, Recharge de 150g (7613034056122) edited by org-nestle-france on 2022-08-28
        </li>
        <li>
            NESCAFÉ SPECIAL FILTRE L'Original Flacon de 200g (3033710074525) edited by org-nestle-france on 2022-08-28
        </li>
        <li>
             (3033710074518) edited by org-nestle-france on 2022-08-28
        </li>
        <li>
            Original (7891000300602) edited by 5m4u9 on 2022-08-27
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
            "subtitle": "last-edits issues related to france brand nestle category coffees",
            "source_url": "https://fr-en.openfoodfacts.org/brand/nestle/category/coffees?sort_by=last_modified_t",
            "elements": [{"element_type": "text", "text_element": "ok"}],
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
    image_url = (
        "https://upload.wikimedia.org/wikipedia/commons/d/d6/"
        "Paziols_%28France%29_Vue_du_village.jpg"
    )
    fake_entity = {
        "description": {"en": "French wine appellation", "fr": "région viticole"},
        "label": {"en": "Fitou AOC", "fr": "Fitou"},
        wikidata_props.image_prop: DictAttr(image_url=image_url),
        wikidata_props.OSM_prop: "2727716",
        wikidata_props.INAO_prop: "6159",
        "attributes": {
            "sitelinks": {
                "enwiki": {"url": "http://en.wikipedia.org/wiki/Fitou_AOC"},
                "frwiki": {"url": "http://fr.wikipedia.org/wiki/Fitou_AOC"},
            }
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
                    "image_url": image_url,
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
    with active_translation("it"):
        # fallbacks to english
        result_it = app.main.wikidata_kp(facet="category", value="fr:fitou")
        assert result_it == expected_result
    with active_translation("fr"):
        # only some items varies
        expected_result_fr = {
            "WikiData": {
                "title": "wiki-data",
                "subtitle": "région viticole",
                "source_url": "https://www.wikidata.org/wiki/Q470974",
                "elements": [
                    {
                        "element_type": "text",
                        "text_element": "Fitou",
                        "image_url": image_url,
                    },
                    {
                        "element_type": "links",
                        "wikipedia": "http://fr.wikipedia.org/wiki/Fitou_AOC",
                        "open_street_map": "https://www.openstreetmap.org/relation/2727716",
                        "INAO": "https://www.inao.gouv.fr/produit/6159",
                    },
                ],
            }
        }
        result_fr = app.main.wikidata_kp(facet="category", value="fr:fitou")
        assert result_fr == expected_result_fr
