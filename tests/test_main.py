import aiohttp
import pytest
import wikidata.client
from fastapi.testclient import TestClient

import app.main
from app.main import app

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
                f"{base_url}/facets/data-quality-errors.json": {
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
    response = client.get(
        "/knowledge_panel?facet_tag=origin&include=last_edits&include=data_quality"
    )
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
                f"{base_url}/facets/packaging/plastic-box/labels/fr:fitou/data-quality-errors.json": {
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
        "&sec_facet_tag=label&sec_value_tag=fr:fitou&country=Germany"
        "&include=data_quality&include=last_edits&include=hunger_game&include=wikidata",
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
