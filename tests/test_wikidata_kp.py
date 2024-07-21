"""separate file for tests of wikidata_kp"""

import aiohttp
import pytest
import wikidata.client

from app.i18n import active_translation
from app.knowledge_panels import KnowledgePanels
from app.wikidata_utils import wikidata_props

from .test_utils import DictAttr, mock_async_get_factory, mock_wikidata_get


@pytest.fixture(autouse=True)
def auto_activate_lang():
    """auto activate translations for each function"""
    with active_translation():
        yield


async def test_wikidata_kp_no_value():
    """wikidata only fetched if there is a value"""
    result = await KnowledgePanels(facet="category").wikidata_kp()
    assert result is None


async def test_wikidata_no_wikidata_property(monkeypatch):
    """first mock the call to open food facts (to get the wikidata property)"""
    expected_url = "https://world.openfoodfacts.org/api/v2/taxonomy"
    expected_kwargs = {
        "params": {
            "tagtype": "categories",
            "fields": "wikidata",
            "tags": "fr:fitou",
        }
    }
    # no wikidata entry !
    json_content = {"fr:fitou": {"parents": []}}
    monkeypatch.setattr(
        aiohttp.ClientSession,
        "get",
        mock_async_get_factory(
            expected_url,
            expected_kwargs,
            json_content,
        ),
    )
    result = await KnowledgePanels(facet="category", value="fr:fitou").wikidata_kp()
    assert result is None


async def test_wikidata_kp(monkeypatch):
    """first mock the call to open food facts (to get the wikidata property)"""
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
        aiohttp.ClientSession,
        "get",
        mock_async_get_factory(
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
    result = await KnowledgePanels(facet="category", value="fr:fitou").wikidata_kp()
    plural_result = await KnowledgePanels(facet="categories", value="fr:fitou").wikidata_kp()
    image_thumb = (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d6/"
        "Paziols_%28France%29_Vue_du_village.jpg/320px-thumbnail.jpg"
    )
    clean_html = (
        f"<p><img alt='wikidata image' src='{image_thumb}'></p>"
        "<li><a href='http://en.wikipedia.org/wiki/Fitou_AOC'>wikipedia</a>"
        "</li>"
        "<li><a href='https://www.openstreetmap.org/relation/2727716'>OpenSteetMap Relation</a>"
        "</li>"
        "<li><a href='https://www.inao.gouv.fr/produit/6159'>INAO relation</a>"
        "</li>"
        "</ul>"
    )
    expected_result = {
        "WikiData": {
            "elements": [
                {
                    "element_type": "text",
                    "text_element": {
                        "html": "<ul><p><em>Fitou AOC</em></p><p>French wine appellation</p>",
                        # noqa: E501
                        "source_text": "wikidata",
                        "source_url": "https://www.wikidata.org/wiki/Q470974",
                    },
                },
                {
                    "element_type": "text",
                    "text_element": {
                        "html": clean_html,
                    },
                },
            ],
            "title_element": {"title": "wikidata"},
        }
    }

    assert result == expected_result
    assert plural_result == expected_result
    with active_translation("it"):
        # fallbacks to english
        result_it = await KnowledgePanels(facet="category", value="fr:fitou").wikidata_kp()
        assert result_it == expected_result
    with active_translation("fr"):
        # only some items varies
        clean_html = (
            f"<p><img alt='wikidata image' src='{image_thumb}'></p>"
            "<li><a href='http://fr.wikipedia.org/wiki/Fitou_AOC'>wikipedia</a>"
            "</li>"
            "<li><a href='https://www.openstreetmap.org/relation/2727716'>OpenSteetMap Relation</a>"
            "</li>"
            "<li><a href='https://www.inao.gouv.fr/produit/6159'>INAO relation</a>"
            "</li>"
            "</ul>"
        )
        expected_result_fr = {
            "WikiData": {
                "elements": [
                    {
                        "element_type": "text",
                        "text_element": {
                            "html": "<ul><p><em>Fitou</em></p><p>région viticole</p>",
                            "source_text": "wikidata",
                            "source_url": "https://www.wikidata.org/wiki/Q470974",
                        },
                    },
                    {
                        "element_type": "text",
                        "text_element": {
                            "html": clean_html,
                        },
                    },
                ],
                "title_element": {"title": "wikidata"},
            }
        }
        result_fr = await KnowledgePanels(facet="category", value="fr:fitou").wikidata_kp()
        assert result_fr == expected_result_fr
