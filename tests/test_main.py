import os

import aiohttp
import pytest
import wikidata.client
from fastapi.testclient import TestClient
from openfoodfacts import Country, Lang

import app.main
from app.information_kp import generate_file_path
from app.main import app
from app.models import KnowledgeContentItem
from app.settings import HTML_DIR

from .test_utils import (
    data_quality_sample,
    last_edits_sample,
    mock_wikidata_get,
    multi_mock_async_get_factory,
    taxonomy_sample,
    wikidata_sample,
)


@pytest.fixture
def client():
    yield TestClient(app)


def test_hello(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Hello from facets-knowledge-panels! Tip: open /docs for documentation"
    }


def test_knowledge_panel_crawl_bot(client):
    response = client.get(
        "/knowledge_panel?facet_tag=packaging&value_tag=plastic-box",
        headers={
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5X Build/MMB29P) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/W.X.Y.Z Mobile Safari/537.36 "
            "(compatible; Googlebot/2.1; +http://www.google.com/bot.html) "
        },
    )
    assert response.status_code == 200
    assert response.json() == {"knowledge_panels": {}}


def test_knowledge_panel_no_value(client, monkeypatch):
    # we do an approximate patching, data is clearly not right, it's just to get some
    base_url = "https://world.openfoodfacts.org"
    monkeypatch.setattr(
        aiohttp.ClientSession,
        "get",
        multi_mock_async_get_factory(
            {
                f"{base_url}/data-quality-errors.json": {
                    "expected_kwargs": None,
                    "json_content": data_quality_sample(base_url),
                },
                f"{base_url}/api/v2/search": {
                    "expected_kwargs": None,
                    "json_content": last_edits_sample(base_url),
                },
            },
        ),
    )
    monkeypatch.setattr(
        wikidata.client.Client,
        "get",
        # this is the entity of taxonomy_sample
        mock_wikidata_get("Q470974", wikidata_sample()),
    )
    response = client.get("/knowledge_panel?facet_tag=origin")
    assert response.status_code == 200
    result = response.json()
    assert set(result["knowledge_panels"].keys()) == {"Quality", "LastEdits"}
    assert len(result["knowledge_panels"]["Quality"]["elements"]) == 1
    assert len(result["knowledge_panels"]["LastEdits"]["elements"]) == 1


def test_knowledge_panel_badendpoint(client):
    response = client.get("/knowledge_panel_bad")
    assert response.status_code == 404


def test_knowledge_panel_with_facet(client, monkeypatch):
    base_url = "https://de-en.openfoodfacts.org"
    monkeypatch.setattr(
        aiohttp.ClientSession,
        "get",
        multi_mock_async_get_factory(
            {
                f"{base_url}/packaging/plastic-box/label/fr:fitou/data-quality-errors.json": {
                    "expected_kwargs": None,
                    "json_content": data_quality_sample(base_url),
                },
                f"{base_url}/api/v2/search": {
                    "expected_kwargs": None,
                    "json_content": last_edits_sample(base_url),
                },
                "https://world.openfoodfacts.org/api/v2/taxonomy": {
                    "expected_kwargs": None,
                    "json_content": taxonomy_sample(),
                },
            },
        ),
    )
    monkeypatch.setattr(
        wikidata.client.Client,
        "get",
        # this is the entity of taxonomy_sample
        mock_wikidata_get("Q470974", wikidata_sample()),
    )
    response = client.get(
        "/knowledge_panel?facet_tag=packaging&value_tag=plastic-box"
        "&sec_facet_tag=label&sec_value_tag=fr:fitou&country=de"
    )
    assert response.status_code == 200
    result = response.json()
    assert set(result["knowledge_panels"].keys()) == {
        "Quality",
        "LastEdits",
        "HungerGames",
        "WikiData",
    }
    assert len(result["knowledge_panels"]["Quality"]["elements"]) == 1
    assert len(result["knowledge_panels"]["LastEdits"]["elements"]) == 1
    assert len(result["knowledge_panels"]["HungerGames"]["elements"]) == 2
    assert len(result["knowledge_panels"]["WikiData"]["elements"]) == 2


@pytest.fixture()
def knowledge_content_item():
    content_item = KnowledgeContentItem(
        lang=Lang.it,
        tag_type="label",
        value_tag="en:specific-label",
        content="Dummy content",
        country=Country.it,
    )
    file_path = generate_file_path(
        HTML_DIR,
        content_item,
    )
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(
        f"<p>DATA about {content_item.value_tag} for "
        f"{content_item.country.value}-{content_item.lang.value}</p>"
    )
    yield content_item
    file_path.unlink()
    os.rmdir(file_path.parent)


def test_knowledge_panel_with_information_kp(client, knowledge_content_item: KnowledgeContentItem):
    for tag_type_suffix in ("", "s"):
        # test with singular and plural form of facet tag
        response = client.get(
            f"/knowledge_panel?facet_tag={knowledge_content_item.tag_type}{tag_type_suffix}"
            f"&value_tag={knowledge_content_item.value_tag}"
            f"&country={knowledge_content_item.country.value}"
            f"&lang_code={knowledge_content_item.lang.value}"
            "&add_contribution_panels=false"
        )
        assert response.status_code == 200
        result = response.json()
        assert set(result["knowledge_panels"].keys()) == {"Description"}
        kp = result["knowledge_panels"]["Description"]
        assert len(kp["elements"]) == 1
        element = kp["elements"][0]
        assert element == {
            "element_type": "text",
            "text_element": {"html": "<p>DATA about en:specific-label for it-it</p>"},
        }


def test_knowledge_panel_with_information_kp_unknown_value(
    client, knowledge_content_item: KnowledgeContentItem
):
    # test with singular and plural form of facet tag
    response = client.get(
        f"/knowledge_panel?facet_tag={knowledge_content_item.tag_type}"
        f"&value_tag=en:value-without-kp"
        f"&country={knowledge_content_item.country.value}"
        f"&lang_code={knowledge_content_item.lang.value}"
        "&add_contribution_panels=false"
    )
    assert response.status_code == 200
    result = response.json()
    assert result["knowledge_panels"] == {}
