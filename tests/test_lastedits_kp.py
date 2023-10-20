"""separate file for tests of lastedits_kp"""
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


async def test_last_edits_kp_with_one_facet_and_value(monkeypatch):
    """test_last_edits_kp_with_one_facet_and_value"""
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
        <p>Total number of edits <b>1 </b></p>
        <li>
            <a class="edit_entry" href="https://hu-en.openfoodfacts.org/product/0715235567418">
                Tiqle Sticks Strawberry taste (0715235567418) edited by packbot on 2022-02-10
            </a>
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
                        "source_url": "https://hu-en.openfoodfacts.org/"
                        "vitamin/vitamin-k?sort_by=last_modified_t",
                        # noqa: E501
                    },
                }
            ],
            "title_element": {"title": "last-edits related to hungary vitamin vitamin-k"},
        }
    }


async def test_last_edits_kp_with_one_facet_and_value_plural_facet(monkeypatch):
    """test_last_edits_kp_with_one_facet_and_value_plural_facet"""
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
        facet="vitamins", value="vitamin-k", country="hungary"
    ).last_edits_kp()
    first_element = result["LastEdits"]["elements"][0]
    first_element["text_element"]["html"] = tidy_html(first_element["text_element"]["html"])
    last_edits_text = """
    <ul>
        <p>Total number of edits <b>1 </b></p>
        <li>
            <a class="edit_entry" href="https://hu-en.openfoodfacts.org/product/0715235567418">
                Tiqle Sticks Strawberry taste (0715235567418) edited by packbot on 2022-02-10
            </a>
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
                        "source_url": "https://hu-en.openfoodfacts.org/vitamin/"
                        "vitamin-k?sort_by=last_modified_t",
                        # noqa: E501
                    },
                }
            ],
            "title_element": {"title": "last-edits related to hungary vitamin vitamin-k"},
        }
    }


async def test_last_edits_kp_with_all_tags(monkeypatch):
    """test_last_edits_kp_with_all_tags"""
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
                "product_name": "Capsules NESCAFE Dolce Gusto" "Cappuccino Extra Crema 16 Capsules",
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
                "product_name": "NESCAFÉ SPECIAL FILTRE L'Original,"
                "Café Soluble, Boîte de 25 Sticks",
                # noqa: E501  # allow long lines
            },
            {
                "code": "3033710074624",
                "last_edit_dates_tags": ["2022-08-28", "2022-08", "2022"],
                "last_editor": "org-nestle-france",
                "product_name": "NESCAFÉ SPECIAL FILTRE Décaféiné," "Café Soluble, Flacon de 200g",
            },
            {
                "code": "7613034056122",
                "last_edit_dates_tags": ["2022-08-28", "2022-08", "2022"],
                "last_editor": "org-nestle-france",
                "product_name": "NESCAFÉ SPECIAL FILTRE L'Original,"
                "Café Soluble, Recharge de 150g",
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
        <p>Total number of edits <b>116</b></p>
        <li>
            <a class="edit_entry" href="https://fr-en.openfoodfacts.org/product/7613036271868">
                "Capsules NESCAFE Dolce GustoCappuccino Extra Crema 16 Capsules"
                "(7613036271868) edited by org-nestle-france on 2022-08-31"
            </a>
        </li>
        <li>
            <a class="edit_entry" href="https://fr-en.openfoodfacts.org/product/7613032655495">
                RICORE Original, Café & Chicorée, Boîte 260g (7613032655495)
                edited by feat on 2022-08-30\
            </a>
        </li>
        <li>
            <a class="edit_entry" href="https://fr-en.openfoodfacts.org/product/7613036303521">
                Ricoré (7613036303521) edited by feat on 2022-08-28
            </a>
        </li>
        <li>
            <a class="edit_entry" href="https://fr-en.openfoodfacts.org/product/3033710072927">
                NESCAFÉ NES, Café Soluble, Boîte de 25 Sticks (2g chacun)
                (3033710072927) edited by org-nestle-france on 2022-08-28\
            </a>
        </li>
        <li>
            <a class="edit_entry" href="https://fr-en.openfoodfacts.org/product/3033710076017">
                NESCAFÉ SPECIAL FILTRE L'Original, Café Soluble, Boîte de 25 Sticks
                (3033710076017) edited by org-nestle-france on 2022-08-28\
            </a>
        </li>
        <li>
            <a class="edit_entry" href="https://fr-en.openfoodfacts.org/product/3033710074624">
                NESCAFÉ SPECIAL FILTRE Décaféiné, Café Soluble, Flacon de 200g
                (3033710074624) edited by org-nestle-france on 2022-08-28\
            </a>
        </li>
        <li>
            <a class="edit_entry" href="https://fr-en.openfoodfacts.org/product/7613034056122">
                NESCAFÉ SPECIAL FILTRE L'Original, Café Soluble, Recharge de 150g
                (7613034056122) edited by org-nestle-france on 2022-08-28\
            </a>
        </li>
        <li>
            <a class="edit_entry" href="https://fr-en.openfoodfacts.org/product/3033710074525">
                NESCAFÉ SPECIAL FILTRE L'Original Flacon de 200g (3033710074525)
                edited by org-nestle-france on 2022-08-28\
            </a>
        </li>
        <li>
            <a class="edit_entry" href="https://fr-en.openfoodfacts.org/product/3033710074518">
                (3033710074518) edited by org-nestle-france on 2022-08-28\
            </a>
        </li>
        <li>
            <a class="edit_entry" href="https://fr-en.openfoodfacts.org/product/7891000300602">
                Original (7891000300602) edited by 5m4u9 on 2022-08-27\
            </a>
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
                        "source_url": "https://fr-en.openfoodfacts.org/brand/"
                        "nestle/category/coffees?sort_by=last_modified_t",
                        # noqa: E501
                    },
                }
            ],
            "title_element": {
                "title": "last-edits related to france brand nestle category coffees"
            },
        }
    }
