from contextlib import asynccontextmanager

from bs4 import BeautifulSoup

from app.wikidata_utils import wikidata_props


class AsyncMockResponse:
    """Mocking aiohttp response object with only the json method"""

    def __init__(self, json_content):
        self.json_content = json_content

    async def json(self):
        return self.json_content


def mock_async_get_factory(target_url, expected_kwargs={}, json_content=None):
    """generate a mock to patch aiohttp.get with a json response

    Use None for target_url and expected_kwargs to avoid checks
    """

    @asynccontextmanager
    async def mock_async_get(session, url, **kwargs):
        if target_url is not None:
            assert url == target_url
        if expected_kwargs is not None:
            assert kwargs == expected_kwargs
        yield AsyncMockResponse(json_content)

    return mock_async_get


def multi_mock_async_get_factory(params_by_url):
    """Multi url version of mock_async_get_factory"""
    mocks = {
        url: mock_async_get_factory(target_url=url, **params)
        for url, params in params_by_url.items()
    }

    @asynccontextmanager
    async def mock_async_get(session, url, **kwargs):
        assert url in mocks, f"No known mock for this url: {url} not in {mocks.keys()}"
        mock = mocks[url]
        async with mock(session, url, **kwargs) as mocked:
            yield mocked

    return mock_async_get


class DictAttr(dict):
    """dict where you can also access values as attributes"""

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)


def mock_wikidata_get(expected_entity, values):
    """Generate a mock to patch wikidata.Client.get with a fake response object

    param str expected_entity: the entity that you want to test is used
    """

    def mock_get(client, entity, *args, **kwargs):
        assert entity == expected_entity
        return DictAttr(values)

    return mock_get


def tidy_html(html):
    """
    Helper function that return pretiffy html
    """
    html = BeautifulSoup(html, "html.parser").prettify()
    return html.strip()


def data_quality_sample(base_url):
    return {
        "count": 181,
        "tags": [
            {
                "id": "en:ecoscore-origins-of-ingredients-origins-are-100-percent-unknown",
                "known": 0,
                "name": "ecoscore-origins-of-ingredients-origins-are-100-percent-unknown",
                "products": 7898,
                "url": (
                    f"{base_url}/" "ecoscore-origins-of-ingredients-origins-are-100-percent-unknown"
                ),
            },
            {
                "id": "en:ecoscore-production-system-no-label",
                "known": 0,
                "name": "ecoscore-production-system-no-label",
                "products": 7883,
                "url": f"{base_url}/ecoscore-production-system-no-label",
            },
            {
                "id": "en:no-packaging-data",
                "known": 0,
                "name": "no-packaging-data",
                "products": 6406,
                "url": f"{base_url}/no-packaging-data",
            },
        ],
    }


def last_edits_sample(base_url):
    return {
        "count": 116,
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
        ],
    }


def taxonomy_sample():
    return {"fr:fitou": {"parents": [], "wikidata": {"en": "Q470974"}}}


def wikidata_sample():
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
    return fake_entity
