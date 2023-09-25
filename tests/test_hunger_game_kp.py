"""separate file for tests of hungergame_kp"""
import pytest

from app.i18n import active_translation
from app.knowledge_panels import KnowledgePanels


@pytest.fixture(autouse=True)
def auto_activate_lang():
    """auto activate translations for each function"""
    with active_translation():
        yield


async def test_hunger_game_kp_no_result():
    """not all facets are compatible with hunger game"""
    result = await KnowledgePanels(
        facet="allergen",
        value="gluten",
        sec_facet="mineral",
        sec_value="zinc",
    ).hunger_game_kp()
    assert result is None


async def test_hunger_game_kp_with_filter_value_and_country():
    """test_hunger_game_kp_with_filter_value_and_country"""
    html = (
        "<ul><li><p><a href='https://hunger.openfoodfacts.org\
        /questions?country=en%3Agermany'>"
        "<em>Answer robotoff questions for country germany</em></a></p></li></ul>"
    )
    result = await KnowledgePanels(
        facet="country", value="germany", country="france"
    ).hunger_game_kp()
    assert result == {
        "HungerGames": {
            "elements": [{"element_type": "text", "text_element": {"html": html}}],
            "title_element": {"title": "Hunger games"},
        }
    }


async def test_hunger_game_kp_with_category():
    """test_hunger_game_kp_with_category"""
    html = (
        "<ul><li><p><a href='https://hunger.openfoodfacts.org/questions?type=category'>"
        "<em>Answer robotoff questions about category</em></a></p></li></ul>"
    )
    result = await KnowledgePanels(facet="category").hunger_game_kp()
    assert result == {
        "HungerGames": {
            "elements": [{"element_type": "text", "text_element": {"html": html}}],
            "title_element": {"title": "Hunger games"},
        }
    }


async def test_hunger_game_kp_category_with_country():
    """test_hunger_game_kp_category_with_country"""
    html0 = (
        "<ul><li><p><a href='https://hunger.openfoodfacts.org/questions?country=en%3Afrance'>"
        "<em>Answer robotoff questions for country france</em></a></p></li></ul>"
    )
    html1 = (
        "<ul><li><p><a href='https://hunger.openfoodfacts.org\
        /questions?country=en%3Afrance&type=category'>"
        "<em>Answer robotoff questions about category for country france</em></a></p></li></ul>"
    )
    result = await KnowledgePanels(facet="category", country="france").hunger_game_kp()
    assert result == {
        "HungerGames": {
            "elements": [
                {"element_type": "text", "text_element": {"html": html0}},
                {"element_type": "text", "text_element": {"html": html1}},
            ],
            "title_element": {"title": "Hunger games"},
        }
    }


async def test_hunger_game_kp_category_with_value():
    """test_hunger_game_kp_category_with_value"""
    html = (
        "<ul><li><p><a href='https://hunger.openfoodfacts.org\
        /questions?type=category&value_tag=en%3Abeers'>"  # noqa: E501
        "<em>Answer robotoff questions about category en:beers</em></a></p></li></ul>"
    )
    result = await KnowledgePanels(facet="category", value="en:beers").hunger_game_kp()
    assert result == {
        "HungerGames": {
            "elements": [{"element_type": "text", "text_element": {"html": html}}],
            "title_element": {"title": "Hunger games"},
        }
    }


async def test_hunger_game_kp_brand_with_value():
    """test_hunger_game_kp_brand_with_value"""
    html = (
        "<ul><li><p>"
        "<a href='https://hunger.openfoodfacts.org/questions?type=brand&value_tag=nestle'>"
        "<em>Answer robotoff questions about brand nestle</em></a></p></li></ul>"
    )
    result = await KnowledgePanels(facet="brand", value="nestle").hunger_game_kp()
    assert result == {
        "HungerGames": {
            "elements": [{"element_type": "text", "text_element": {"html": html}}],
            "title_element": {"title": "Hunger games"},
        }
    }


async def test_hunger_game_kp_label_with_value():
    """test_hunger_game_kp_label_with_value"""
    html = (
        "<ul><li><p><a href='https://hunger.openfoodfacts.org\
        /questions?type=label&value_tag=en%3Aorganic'>"
        "<em>Answer robotoff questions about label en:organic</em></a></p></li></ul>"
    )
    result = await KnowledgePanels(facet="label", value="en:organic").hunger_game_kp()
    assert result == {
        "HungerGames": {
            "elements": [{"element_type": "text", "text_element": {"html": html}}],
            "title_element": {"title": "Hunger games"},
        }
    }


async def test_hunger_game_kp_label_with_value_plural_facet():
    """test_hunger_game_kp_label_with_value_plural_facet"""
    html = (
        "<ul><li><p><a href='https://hunger.openfoodfacts.org\
        /questions?type=label&value_tag=en%3Aorganic'>"
        "<em>Answer robotoff questions about label en:organic</em></a></p></li></ul>"
    )
    result = await KnowledgePanels(facet="labels", value="en:organic").hunger_game_kp()
    assert result == {
        "HungerGames": {
            "elements": [{"element_type": "text", "text_element": {"html": html}}],
            "title_element": {"title": "Hunger games"},
        }
    }


async def test_HungerGame_double_country_and_value():
    """test_HungerGame_double_country_and_value"""
    # facet country have priority
    html1 = (
        "<ul><li><p><a href='https://hunger.openfoodfacts.org/questions?country=en%3Afrance'>"
        "<em>Answer robotoff questions for country france</em></a></p></li></ul>"
    )
    html2 = (
        "<ul><li><p><a href='https://hunger.openfoodfacts.org\
        /questions?country=en%3Afrance&type=category&value_tag=beers'>"  # noqa:E501
        "<em>Answer robotoff questions about category beers for country france\
        </em></a></p></li></ul>"
    )
    kp = KnowledgePanels(
        facet="country",
        value="en:france",
        country="germany",
        sec_facet="category",
        sec_value="beers",
    )
    result = await kp.hunger_game_kp()
    assert result == {
        "HungerGames": {
            "title_element": {"title": "Hunger games"},
            "elements": [
                {
                    "element_type": "text",
                    "text_element": {
                        "html": html1,
                    },
                },
                {
                    "element_type": "text",
                    "text_element": {
                        "html": html2,
                    },
                },
            ],
        }
    }


async def test_hunger_game_kp_with_all_tag_1():
    """test_hunger_game_kp_with_all_tag_1"""
    html0 = (
        "<ul><li><p><a href='https://hunger.openfoodfacts.org\
        /questions?country=en%3Afrance&brand=lidl'>"
        "<em>Answer robotoff questions for country france for brand lidl\
        </em></a></p></li></ul>"
    )
    html1 = (
        "<ul><li><p><a href='https://hunger.openfoodfacts.org\
        /questions?country=en%3Afrance&brand=lidl&type=category&value_tag=en%3Abeers'>"
        # noqa: E501
        "<em>Answer robotoff questions about category en:beers for country\
        france for brand lidl</em></a></p></li></ul>"  # noqa: E501
    )
    assert await KnowledgePanels(
        facet="category",
        value="en:beers",
        sec_facet="brand",
        sec_value="lidl",
        country="france",
    ).hunger_game_kp() == {
        "HungerGames": {
            "elements": [
                {"element_type": "text", "text_element": {"html": html0}},
                {"element_type": "text", "text_element": {"html": html1}},
            ],
            "title_element": {"title": "Hunger games"},
        }
    }


async def test_hunger_game_kp_with_all_tag_2():
    """test_hunger_game_kp_with_all_tag_2"""
    html0 = (
        "<ul><li><p><a href='https://hunger.openfoodfacts.org/questions?type=brand'>"
        "<em>Answer robotoff questions about brand</em></a></p></li></ul>"
    )
    html1 = (
        "<ul><li><p><a href='https://hunger.openfoodfacts.org\
        /questions?type=category&value_tag=en%3Acoffees'>"
        # noqa: E501
        "<em>Answer robotoff questions about category en:coffees</em></a></p></li></ul>"
    )
    assert await KnowledgePanels(
        facet="brand",
        sec_facet="category",
        sec_value="en:coffees",
    ).hunger_game_kp() == {
        "HungerGames": {
            "elements": [
                {"element_type": "text", "text_element": {"html": html0}},
                {"element_type": "text", "text_element": {"html": html1}},
            ],
            "title_element": {"title": "Hunger games"},
        }
    }


async def test_hunger_game_kp_with_all_tag_3():
    """test_hunger_game_kp_with_all_tag_3"""
    html0 = (
        "<ul><li><p><a href='https://hunger.openfoodfacts.org\
        /questions?country=en%3Aitaly'>"
        "<em>Answer robotoff questions for country italy</em></a></p></li></ul>"
    )
    html1 = (
        "<ul><li><p><a href='https://hunger.openfoodfacts.org\
        /questions?country=en%3Aitaly&type=category&value_tag=en%3Ameals'>"  # noqa: E501
        "<em>Answer robotoff questions about category en:meals for country italy</em></a>"
        "</p></li></ul>"
    )
    html2 = (
        "<ul><li><p><a href='https://hunger.openfoodfacts.org\
        /questions?country=en%3Aitaly&type=label&value_tag=vegan'>"  # noqa: E501
        "<em>Answer robotoff questions about label vegan for country italy</em></a>"
        "</p></li></ul>"
    )
    assert await KnowledgePanels(
        facet="category",
        value="en:meals",
        sec_facet="label",
        sec_value="vegan",
        country="italy",
    ).hunger_game_kp() == {
        "HungerGames": {
            "elements": [
                {"element_type": "text", "text_element": {"html": html0}},
                {"element_type": "text", "text_element": {"html": html1}},
                {"element_type": "text", "text_element": {"html": html2}},
            ],
            "title_element": {"title": "Hunger games"},
        }
    }
