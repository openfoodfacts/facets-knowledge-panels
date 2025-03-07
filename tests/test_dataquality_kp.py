"""seperate file for tests of dataquality_kp"""

import aiohttp
import pytest

from app.i18n import active_translation
from app.knowledge_panels import KnowledgePanels

from .test_utils import mock_async_get_factory, tidy_html


@pytest.fixture(autouse=True)
def auto_activate_lang():
    """auto activate translations for each function"""
    with active_translation():
        yield


async def test_data_quality_kp_with_world(monkeypatch):
    """test_data_quality_kp_with_world"""
    expected_url = "https://world.openfoodfacts.org/data-quality-errors.json"
    base_url = "https://world.openfoodfacts.org/data-quality-errors"
    json_content = {
        "count": 129,
        "tags": [
            {
                "id": "en:ecoscore-production-system-no-label",
                "known": 0,
                "name": "ecoscore-production-system-no-label",
                "products": 1848,
                "url": f"{base_url}/ecoscore-production-system-no-label",
            },
            {
                "id": "en:no-packaging-data",
                "known": 0,
                "name": "no-packaging-data",
                "products": 1788,
                "url": f"{base_url}/no-packaging-data",
            },
            {
                "id": "en:ecoscore-origins-of-ingredients-origins-are-100-percent-unknown",
                "known": 0,
                "name": "ecoscore-origins-of-ingredients-origins-are-100-percent-unknown",
                "products": 1778,
                "url": (
                    f"{base_url}/" "ecoscore-origins-of-ingredients-origins-are-100-percent-unknown"
                ),
            },
        ],
    }

    monkeypatch.setattr(
        aiohttp.ClientSession,
        "get",
        mock_async_get_factory(expected_url, json_content=json_content),
    )
    result = await KnowledgePanels(facet="world").data_quality_kp()
    first_element = result["Quality"]["elements"][0]
    first_element["text_element"]["html"] = tidy_html(first_element["text_element"]["html"])
    expected_text = """
    <ul>
        <p>The total number of issues are <b>129</b></p>
        <li>
            <a href="https://world.openfoodfacts.org/data-quality-errors/ecoscore-production-system-no-label">1848 products with ecoscore-production-system-no-label</a>
        </li>
        <li>
            <a href="https://world.openfoodfacts.org/data-quality-errors/no-packaging-data">1788 products with no-packaging-data</a>
        </li>
        <li>
            <a href="https://world.openfoodfacts.org/data-quality-errors/ecoscore-origins-of-ingredients-origins-are-100-percent-unknown">1778 products with ecoscore-origins-of-ingredients-origins-are-100-percent-unknown</a>
        </li>
    </ul>
    """  # noqa: E501  # allow long lines
    # assert html separately to have better output in case of error
    assert first_element["text_element"]["html"] == tidy_html(expected_text)
    # now replace it for concision of output
    first_element["text_element"]["html"] = "ok"
    assert result == {
        "Quality": {
            "elements": [
                {
                    "element_type": "text",
                    "text_element": {
                        "html": "ok",
                        "source_text": "Data-quality issues",
                        "source_url": "https://world.openfoodfacts.org/data-quality-errors",
                    },
                }
            ],
            "title_element": {"title": "Data-quality issues related to "},
        }
    }


async def test_data_quality_kp_with_country(monkeypatch):
    """test_data_quality_kp_with_country"""
    expected_url = "https://tr-en.openfoodfacts.org/data-quality-errors.json"
    base_url = "https://tr-en.openfoodfacts.org/data-quality-errors"
    json_content = {
        "count": 129,
        "tags": [
            {
                "id": "en:ecoscore-production-system-no-label",
                "known": 0,
                "name": "ecoscore-production-system-no-label",
                "products": 1848,
                "url": f"{base_url}/ecoscore-production-system-no-label",
            },
            {
                "id": "en:no-packaging-data",
                "known": 0,
                "name": "no-packaging-data",
                "products": 1788,
                "url": f"{base_url}/no-packaging-data",
            },
            {
                "id": "en:ecoscore-origins-of-ingredients-origins-are-100-percent-unknown",
                "known": 0,
                "name": "ecoscore-origins-of-ingredients-origins-are-100-percent-unknown",
                "products": 1778,
                "url": (
                    f"{base_url}/" "ecoscore-origins-of-ingredients-origins-are-100-percent-unknown"
                ),
            },
        ],
    }

    monkeypatch.setattr(
        aiohttp.ClientSession,
        "get",
        mock_async_get_factory(expected_url, json_content=json_content),
    )
    result = await KnowledgePanels(
        facet="country", value="Turkey", country="Hungary"
    ).data_quality_kp()
    first_element = result["Quality"]["elements"][0]
    first_element["text_element"]["html"] = tidy_html(first_element["text_element"]["html"])
    expected_text = """
    <ul>
        <p>The total number of issues are <b>129</b></p>
        <li>
            <a href="https://tr-en.openfoodfacts.org/data-quality-errors/ecoscore-production-system-no-label">1848 products with ecoscore-production-system-no-label</a>
        </li>
        <li>
            <a href="https://tr-en.openfoodfacts.org/data-quality-errors/no-packaging-data">1788 products with no-packaging-data</a>
        </li>
        <li>
            <a href="https://tr-en.openfoodfacts.org/data-quality-errors/ecoscore-origins-of-ingredients-origins-are-100-percent-unknown">1778 products with ecoscore-origins-of-ingredients-origins-are-100-percent-unknown</a>
        </li>
    </ul>
    """  # noqa: E501  # allow long lines
    # assert html separately to have better output in case of error
    assert first_element["text_element"]["html"] == tidy_html(expected_text)
    # now replace it for concision of output
    first_element["text_element"]["html"] = "ok"
    assert result == {
        "Quality": {
            "elements": [
                {
                    "element_type": "text",
                    "text_element": {
                        "html": "ok",
                        "source_text": "Data-quality issues",
                        "source_url": "https://tr-en.openfoodfacts.org/data-quality-errors",
                    },
                }
            ],
            "title_element": {"title": "Data-quality issues related to Turkey "},
        }
    }


async def test_data_quality_kp_with_one_facet_and_value(monkeypatch):
    """test_data_quality_kp_with_one_facet_and_value"""
    expected_url = "https://world.openfoodfacts.org/brand/lidl/data-quality-errors.json"
    base_url = "https://world.openfoodfacts.org/brand/lidl/data-quality-errors"
    json_content = {
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

    monkeypatch.setattr(
        aiohttp.ClientSession,
        "get",
        mock_async_get_factory(expected_url, json_content=json_content),
    )
    result = await KnowledgePanels(facet="brand", value="lidl").data_quality_kp()
    first_element = result["Quality"]["elements"][0]
    first_element["text_element"]["html"] = tidy_html(first_element["text_element"]["html"])
    expected_text = """
    <ul>
        <p>The total number of issues are <b>181</b></p>
        <li>
            <a href="https://world.openfoodfacts.org/brand/lidl/data-quality-errors/ecoscore-origins-of-ingredients-origins-are-100-percent-unknown">7898 products with ecoscore-origins-of-ingredients-origins-are-100-percent-unknown</a>
        </li>
        <li>
            <a href="https://world.openfoodfacts.org/brand/lidl/data-quality-errors/ecoscore-production-system-no-label">7883 products with ecoscore-production-system-no-label</a>
        </li>
        <li>
            <a href="https://world.openfoodfacts.org/brand/lidl/data-quality-errors/no-packaging-data">6406 products with no-packaging-data</a>
        </li>
    </ul>
    """  # noqa: E501  # allow long lines
    # assert html separately to have better output in case of error
    assert first_element["text_element"]["html"] == tidy_html(expected_text)
    # now replace it for concision of output
    first_element["text_element"]["html"] = "ok"
    assert result == {
        "Quality": {
            "elements": [
                {
                    "element_type": "text",
                    "text_element": {
                        "html": "ok",
                        "source_text": "Data-quality issues",
                        "source_url": "https://world.openfoodfacts.org/brand/lidl/"
                        + "data-quality-errors",
                    },
                }
            ],
            "title_element": {"title": "Data-quality issues related to brand lidl"},
        }
    }


async def test_data_quality_kp_with_one_facet_and_value_plural_facet(monkeypatch):
    """test_data_quality_kp_with_one_facet_and_value_plural_facet"""
    expected_url = "https://world.openfoodfacts.org/brand/lidl/data-quality-errors.json"
    base_url = "https://world.openfoodfacts.org/brand/lidl/data-quality-errors"
    json_content = {
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

    monkeypatch.setattr(
        aiohttp.ClientSession,
        "get",
        mock_async_get_factory(expected_url, json_content=json_content),
    )
    result = await KnowledgePanels(facet="brands", value="lidl").data_quality_kp()
    first_element = result["Quality"]["elements"][0]
    first_element["text_element"]["html"] = tidy_html(first_element["text_element"]["html"])
    expected_text = """
    <ul>
        <p>The total number of issues are <b>181</b></p>
        <li>
            <a href="https://world.openfoodfacts.org/brand/lidl/data-quality-errors/ecoscore-origins-of-ingredients-origins-are-100-percent-unknown">7898 products with ecoscore-origins-of-ingredients-origins-are-100-percent-unknown</a>
        </li>
        <li>
            <a href="https://world.openfoodfacts.org/brand/lidl/data-quality-errors/ecoscore-production-system-no-label">7883 products with ecoscore-production-system-no-label</a>
        </li>
        <li>
            <a href="https://world.openfoodfacts.org/brand/lidl/data-quality-errors/no-packaging-data">6406 products with no-packaging-data</a>
        </li>
    </ul>
    """  # noqa: E501  # allow long lines
    # assert html separately to have better output in case of error
    assert first_element["text_element"]["html"] == tidy_html(expected_text)
    # now replace it for concision of output
    first_element["text_element"]["html"] = "ok"
    assert result == {
        "Quality": {
            "elements": [
                {
                    "element_type": "text",
                    "text_element": {
                        "html": "ok",
                        "source_text": "Data-quality issues",
                        "source_url": "https://world.openfoodfacts.org/brand/lidl/"
                        + "data-quality-errors",
                    },
                }
            ],
            "title_element": {"title": "Data-quality issues related to brand lidl"},
        }
    }


async def test_data_quality_kp_with_all_tags(monkeypatch):
    """test_data_quality_kp_with_all_tags"""
    expected_url = (
        "https://world.openfoodfacts.org/category/beers/brand/budweiser/data-quality-errors.json"
    )
    json_content = {
        "count": 24,
        "tags": [
            {
                "id": "en:alcoholic-beverages-category-without-alcohol-value",
                "known": 0,
                "name": "alcoholic-beverages-category-without-alcohol-value",
                "products": 13,
                "url": "https://world.openfoodfacts.org/category/beers/"
                + "data-quality-errors/alcoholic-beverages-category-without-alcohol-value",
                # noqa: E501  # allow long lines
            },
            {
                "id": "en:ecoscore-production-system-no-label",
                "known": 0,
                "name": "ecoscore-production-system-no-label",
                "products": 13,
                "url": "https://world.openfoodfacts.org/category/beers/"
                "data-quality-errors/ecoscore-production-system-no-label",
                # noqa: E501  # allow long lines
            },
            {
                "id": "en:ecoscore-origins-of-ingredients-origins-are-100-percent-unknown",
                "known": 0,
                "name": "ecoscore-origins-of-ingredients-origins-are-100-percent-unknown",
                "products": 12,
                "url": "https://world.openfoodfacts.org/category/beers/data-quality-errors/"
                "ecoscore-origins-of-ingredients-origins-are-100-percent-unknown",
                # noqa: E501  # allow long lines
            },
        ],
    }

    monkeypatch.setattr(
        aiohttp.ClientSession,
        "get",
        mock_async_get_factory(expected_url, json_content=json_content),
    )
    result = await KnowledgePanels(
        facet="category", value="beers", sec_facet="brand", sec_value="budweiser"
    ).data_quality_kp()
    first_element = result["Quality"]["elements"][0]
    first_element["text_element"]["html"] = tidy_html(first_element["text_element"]["html"])
    expected_text = """
    <ul>
        <p>The total number of issues are <b>24</b></p>
        <li>
            <a href="https://world.openfoodfacts.org/category/beers/data-quality-errors/alcoholic-beverages-category-without-alcohol-value">13 products with alcoholic-beverages-category-without-alcohol-value</a>
        </li>
        <li>
            <a href="https://world.openfoodfacts.org/category/beers/data-quality-errors/ecoscore-production-system-no-label">13 products with ecoscore-production-system-no-label</a>
        </li>
        <li>
            <a href="https://world.openfoodfacts.org/category/beers/data-quality-errors/ecoscore-origins-of-ingredients-origins-are-100-percent-unknown">12 products with ecoscore-origins-of-ingredients-origins-are-100-percent-unknown</a>
        </li>
    </ul>
    """  # noqa: E501  # allow long lines
    # assert html separately to have better output in case of error
    assert first_element["text_element"]["html"] == tidy_html(expected_text)
    # now replace it for concision of output
    first_element["text_element"]["html"] = "ok"
    assert result == {
        "Quality": {
            "elements": [
                {
                    "element_type": "text",
                    "text_element": {
                        "html": "ok",
                        "source_text": "Data-quality issues",
                        "source_url": "https://world.openfoodfacts.org/category/beers/"
                        + "brand/budweiser/data-quality-errors",
                        # noqa: E501
                    },
                }
            ],
            "title_element": {
                "title": "Data-quality issues related to category beers brand budweiser"
            },
        }
    }
