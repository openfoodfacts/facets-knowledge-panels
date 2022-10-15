import aiohttp
import pytest
import wikidata.client

from app.i18n import active_translation
from app.knowledge_panels import KnowledgePanels
from app.wikidata_utils import wikidata_props

from .test_utils import DictAttr, mock_async_get_factory, mock_wikidata_get, tidy_html


@pytest.fixture(autouse=True)
def auto_activate_lang():
    """auto activate translations for each function"""
    with active_translation():
        yield


async def test_hunger_game_kp_with_filter_value_and_country():
    html = (
        "<p><a href='https://hunger.openfoodfacts.org/questions?country=en%3Agermany'>"
        "Answer robotoff questions about germany</a></p>"
    )
    assert await KnowledgePanels(
        facet="country", value="germany", country="france"
    ).hunger_game_kp() == {
        "hunger_game": {
            "elements": [{"element_type": "text", "text_element": {"html": html}}],
            "title_element": {"title": "hunger-games"},
        }
    }


async def test_hunger_game_kp_with_category():
    html = (
        "<p><a href='https://hunger.openfoodfacts.org/questions?type=category'>"
        "Answer robotoff questions about category</a></p>"
    )
    assert await KnowledgePanels(facet="category").hunger_game_kp() == {
        "hunger_game": {
            "elements": [{"element_type": "text", "text_element": {"html": html}}],
            "title_element": {"title": "hunger-games"},
        }
    }


async def test_hunger_game_kp_category_with_country():
    html0 = (
        "<p><a href='https://hunger.openfoodfacts.org/questions?country=en%3Afrance'>"
        "Answer robotoff questions about for country france</a></p>"
    )
    html1 = (
        "<p><a href='https://hunger.openfoodfacts.org/questions?country=en%3Afrance&type=category'>"
        "Answer robotoff questions about category  for country france</a></p>"
    )
    assert await KnowledgePanels(facet="category", country="france").hunger_game_kp() == {
        "hunger_game": {
            "elements": [
                {"element_type": "text", "text_element": {"html": html0}},
                {"element_type": "text", "text_element": {"html": html1}},
            ],
            "title_element": {"title": "hunger-games"},
        }
    }


async def test_hunger_game_kp_category_with_value():
    html = (
        "<p><a href='https://hunger.openfoodfacts.org/questions?type=category&value_tag=en%3Abeers'>"  # noqa: E501
        "Answer robotoff questions about category en:beers</a></p>"
    )
    assert await KnowledgePanels(facet="category", value="en:beers").hunger_game_kp() == {
        "hunger_game": {
            "elements": [{"element_type": "text", "text_element": {"html": html}}],
            "title_element": {"title": "hunger-games"},
        }
    }


async def test_hunger_game_kp_brand_with_value():
    html = (
        "<p><a href='https://hunger.openfoodfacts.org/questions?type=brand&value_tag=nestle'>"
        "Answer robotoff questions about brand nestle</a></p>"
    )
    assert await KnowledgePanels(facet="brand", value="nestle").hunger_game_kp() == {
        "hunger_game": {
            "elements": [{"element_type": "text", "text_element": {"html": html}}],
            "title_element": {"title": "hunger-games"},
        }
    }


async def test_hunger_game_kp_label_with_value():
    html = (
        "<p><a href='https://hunger.openfoodfacts.org/questions?type=label&value_tag=en%3Aorganic'>"
        "Answer robotoff questions about label en:organic</a></p>"
    )
    assert await KnowledgePanels(facet="label", value="en:organic").hunger_game_kp() == {
        "hunger_game": {
            "elements": [{"element_type": "text", "text_element": {"html": html}}],
            "title_element": {"title": "hunger-games"},
        }
    }


async def test_hunger_game_kp_with_all_tag_1():
    html0 = (
        "<p><a href='https://hunger.openfoodfacts.org/questions?country=en%3Afrance&brand=lidl'>"
        "Answer robotoff questions about for country france for brand lidl</a></p>"
    )
    html1 = (
        "<p><a href='https://hunger.openfoodfacts.org/questions?country=en%3Afrance&brand=lidl&type=category&value_tag=en%3Abeers'>"  # noqa: E501
        "Answer robotoff questions about category en:beers for country france for brand lidl</a></p>"  # noqa: E501
    )
    assert await KnowledgePanels(
        facet="category",
        value="en:beers",
        sec_facet="brand",
        sec_value="lidl",
        country="france",
    ).hunger_game_kp() == {
        "hunger_game": {
            "elements": [
                {"element_type": "text", "text_element": {"html": html0}},
                {"element_type": "text", "text_element": {"html": html1}},
            ],
            "title_element": {"title": "hunger-games"},
        }
    }


async def test_hunger_game_kp_with_all_tag_2():

    html0 = (
        "<p><a href='https://hunger.openfoodfacts.org/questions?type=brand'>"
        "Answer robotoff questions about brand</a></p>"
    )
    html1 = (
        "<p><a href='https://hunger.openfoodfacts.org/questions?type=category&value_tag=en%3Acoffees'>"  # noqa: E501
        "Answer robotoff questions about category en:coffees</a></p>"
    )
    assert await KnowledgePanels(
        facet="brand",
        sec_facet="category",
        sec_value="en:coffees",
    ).hunger_game_kp() == {
        "hunger_game": {
            "elements": [
                {"element_type": "text", "text_element": {"html": html0}},
                {"element_type": "text", "text_element": {"html": html1}},
            ],
            "title_element": {"title": "hunger-games"},
        }
    }


async def test_hunger_game_kp_with_all_tag_3():
    html0 = (
        "<p><a href='https://hunger.openfoodfacts.org/questions?country=en%3Aitaly'>"
        "Answer robotoff questions about for country italy</a></p>"
    )
    html1 = (
        "<p><a href='https://hunger.openfoodfacts.org/questions?country=en%3Aitaly&type=category&value_tag=en%3Ameals'>"  # noqa: E501
        "Answer robotoff questions about category en:meals for country italy</a></p>"
    )
    html2 = (
        "<p><a href='https://hunger.openfoodfacts.org/questions?country=en%3Aitaly&type=label&value_tag=vegan'>"  # noqa: E501
        "Answer robotoff questions about label vegan for country italy</a></p>"
    )
    assert await KnowledgePanels(
        facet="category",
        value="en:meals",
        sec_facet="label",
        sec_value="vegan",
        country="italy",
    ).hunger_game_kp() == {
        "hunger_game": {
            "elements": [
                {"element_type": "text", "text_element": {"html": html0}},
                {"element_type": "text", "text_element": {"html": html1}},
                {"element_type": "text", "text_element": {"html": html2}},
            ],
            "title_element": {"title": "hunger-games"},
        }
    }


async def test_data_quality_kp_with_country(monkeypatch):
    expected_url = "https://tr-en.openfoodfacts.org/data-quality.json"
    base_url = "https://tr-en.openfoodfacts.org/data-quality"
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
        <p>The total number of issues are 129</p>
        <li>
            <a href="https://tr-en.openfoodfacts.org/data-quality/ecoscore-production-system-no-label">1848 products with ecoscore-production-system-no-label</a>
        </li>
        <li>
            <a href="https://tr-en.openfoodfacts.org/data-quality/no-packaging-data">1788 products with no-packaging-data</a>
        </li>
        <li>
            <a href="https://tr-en.openfoodfacts.org/data-quality/ecoscore-origins-of-ingredients-origins-are-100-percent-unknown">1778 products with ecoscore-origins-of-ingredients-origins-are-100-percent-unknown</a>
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
                        "source_url": "https://tr-en.openfoodfacts.org/data-quality",
                    },
                }
            ],
            "title_element": {"title": "Data-quality issues related to Turkey "},
        }
    }


async def test_data_quality_kp_with_one_facet_and_value(monkeypatch):
    expected_url = "https://world.openfoodfacts.org/brand/lidl/data-quality.json"
    base_url = "https://world.openfoodfacts.org/brand/lidl/data-quality"
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
        <p>The total number of issues are 181</p>
        <li>
            <a href="https://world.openfoodfacts.org/brand/lidl/data-quality/ecoscore-origins-of-ingredients-origins-are-100-percent-unknown">7898 products with ecoscore-origins-of-ingredients-origins-are-100-percent-unknown</a>
        </li>
        <li>
            <a href="https://world.openfoodfacts.org/brand/lidl/data-quality/ecoscore-production-system-no-label">7883 products with ecoscore-production-system-no-label</a>
        </li>
        <li>
            <a href="https://world.openfoodfacts.org/brand/lidl/data-quality/no-packaging-data">6406 products with no-packaging-data</a>
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
                        "source_url": "https://world.openfoodfacts.org/brand/lidl/data-quality",
                    },
                }
            ],
            "title_element": {"title": "Data-quality issues related to brand lidl"},
        }
    }


async def test_data_quality_kp_with_all_tags(monkeypatch):
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
                "url": "https://world.openfoodfacts.org/category/beers/data-quality/alcoholic-beverages-category-without-alcohol-value",  # noqa: E501  # allow long lines
            },
            {
                "id": "en:ecoscore-production-system-no-label",
                "known": 0,
                "name": "ecoscore-production-system-no-label",
                "products": 13,
                "url": "https://world.openfoodfacts.org/category/beers/data-quality/ecoscore-production-system-no-label",  # noqa: E501  # allow long lines
            },
            {
                "id": "en:ecoscore-origins-of-ingredients-origins-are-100-percent-unknown",
                "known": 0,
                "name": "ecoscore-origins-of-ingredients-origins-are-100-percent-unknown",
                "products": 12,
                "url": "https://world.openfoodfacts.org/category/beers/data-quality/ecoscore-origins-of-ingredients-origins-are-100-percent-unknown",  # noqa: E501  # allow long lines
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
        <p>The total number of issues are 24</p>
        <li>
            <a href="https://world.openfoodfacts.org/category/beers/data-quality/alcoholic-beverages-category-without-alcohol-value">13 products with alcoholic-beverages-category-without-alcohol-value</a>
        </li>
        <li>
            <a href="https://world.openfoodfacts.org/category/beers/data-quality/ecoscore-production-system-no-label">13 products with ecoscore-production-system-no-label</a>
        </li>
        <li>
            <a href="https://world.openfoodfacts.org/category/beers/data-quality/ecoscore-origins-of-ingredients-origins-are-100-percent-unknown">12 products with ecoscore-origins-of-ingredients-origins-are-100-percent-unknown</a>
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
                        "source_url": "https://world.openfoodfacts.org/category/beers/brand/budweiser/data-quality",  # noqa: E501
                    },
                }
            ],
            "title_element": {
                "title": "Data-quality issues related to category beers brand budweiser"
            },
        }
    }


async def test_last_edits_kp_with_one_facet_and_value(monkeypatch):
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
        aiohttp.ClientSession,
        "get",
        mock_async_get_factory(
            expected_url,
            expected_kwargs,
            json_content,
        ),
    )
    result = await KnowledgePanels(
        facet="vitamin", value="vitamin-k", country="hungary"
    ).last_edits_kp()
    first_element = result["LastEdits"]["elements"][0]
    first_element["text_element"]["html"] = tidy_html(first_element["text_element"]["html"])
    last_edits_text = """
    <ul>
        <p>Total number of edits 1 </p>
        <li>
            Tiqle Sticks Strawberry taste (0715235567418) edited by packbot on 2022-02-10
        </li>
    </ul>
    """
    # assert html separately to have better output in case of error
    assert first_element["text_element"]["html"] == tidy_html(last_edits_text)
    # now replace it for concision of output
    first_element["text_element"]["html"] = "ok"
    assert result == {
        "LastEdits": {
            "elements": [
                {
                    "element_type": "text",
                    "text_element": {
                        "html": "ok",
                        "source_text": "Last-edits",
                        "source_url": "https://hu-en.openfoodfacts.org/vitamin/vitamin-k?sort_by=last_modified_t",  # noqa: E501
                    },
                }
            ],
            "title_element": {"title": "last-edits issues related to hungary vitamin vitamin-k"},
        }
    }


async def test_last_edits_kp_with_all_tags(monkeypatch):
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
            {
                "code": "3033710076017",
                "last_edit_dates_tags": ["2022-08-28", "2022-08", "2022"],
                "last_editor": "org-nestle-france",
                "product_name": "NESCAFÉ SPECIAL FILTRE L'Original, Café Soluble, Boîte de 25 Sticks",  # noqa: E501  # allow long lines
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
        aiohttp.ClientSession,
        "get",
        mock_async_get_factory(
            expected_url,
            expected_kwargs,
            json_content,
        ),
    )
    result = await KnowledgePanels(
        facet="brand",
        value="nestle",
        sec_facet="category",
        sec_value="coffees",
        country="france",
    ).last_edits_kp()
    first_element = result["LastEdits"]["elements"][0]
    first_element["text_element"]["html"] = tidy_html(first_element["text_element"]["html"])
    last_edits_text = """
    <ul>
        <p>Total number of edits 116</p>
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
    """  # noqa: E501  # allow long lines
    # assert html separately to have better output in case of error
    assert first_element["text_element"]["html"] == tidy_html(last_edits_text)
    # now replace it for concision of output
    first_element["text_element"]["html"] = "ok"
    assert result == {
        "LastEdits": {
            "elements": [
                {
                    "element_type": "text",
                    "text_element": {
                        "html": "ok",
                        "source_text": "Last-edits",
                        "source_url": "https://fr-en.openfoodfacts.org/brand/nestle/category/coffees?sort_by=last_modified_t",  # noqa: E501
                    },
                }
            ],
            "title_element": {
                "title": "last-edits issues related to france brand nestle category coffees"
            },
        }
    }


async def test_wikidata_kp(monkeypatch):
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
    expected_result = {
        "WikiData": {
            "elements": [
                {
                    "element_type": "text",
                    "text_element": {
                        "source_label": "Fitou AOC",
                        "source_description": "French wine appellation",
                        "source_text": "wikidata",
                        "source_url": "https://www.wikidata.org/wiki/Q470974",
                    },
                },
                {
                    "element_type": "links",
                    "link_element": {
                        "wikipedia": "http://en.wikipedia.org/wiki/Fitou_AOC",
                        "image_url": image_url,
                        "open_street_map": "https://www.openstreetmap.org/relation/2727716",
                        "INAO": "https://www.inao.gouv.fr/produit/6159",
                    },
                },
            ],
            "title_element": {"title": "wikidata"},
        }
    }

    assert result == expected_result
    with active_translation("it"):
        # fallbacks to english
        result_it = await KnowledgePanels(facet="category", value="fr:fitou").wikidata_kp()
        assert result_it == expected_result
    with active_translation("fr"):
        # only some items varies
        expected_result_fr = {
            "WikiData": {
                "elements": [
                    {
                        "element_type": "text",
                        "text_element": {
                            "source_label": "Fitou",
                            "source_description": "région viticole",
                            "source_text": "wikidata",
                            "source_url": "https://www.wikidata.org/wiki/Q470974",
                        },
                    },
                    {
                        "element_type": "links",
                        "link_element": {
                            "wikipedia": "http://fr.wikipedia.org/wiki/Fitou_AOC",
                            "image_url": image_url,
                            "open_street_map": "https://www.openstreetmap.org/relation/2727716",
                            "INAO": "https://www.inao.gouv.fr/produit/6159",
                        },
                    },
                ],
                "title_element": {"title": "wikidata"},
            }
        }
        result_fr = await KnowledgePanels(facet="category", value="fr:fitou").wikidata_kp()
        assert result_fr == expected_result_fr
