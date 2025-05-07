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
        "<ul><li><p><a href='https://hunger.openfoodfacts.org/questions?country=en%3Agermany' "
        "class='button small'><em>Answer questions from Robotoff for the country - Germany"
        "</em></a></p></li></ul>"
    )
    result = await KnowledgePanels(
        facet="country", value="germany", country="france"
    ).hunger_game_kp()
    assert result == {
        "HungerGames": {
            "elements": [{"element_type": "text", "text_element": {"html": html}}],
            "title_element": {"title": "Hunger Games (Contribute by playing)"},
        }
    }


async def test_hunger_game_kp_with_category():
    """test_hunger_game_kp_with_category"""
    html = (
        "<ul><li><p><a href='https://hunger.openfoodfacts.org/questions?type=category' "
        "class='button small'><em>Answer questions from Robotoff about the category"
        "</em></a></p></li></ul>"
    )
    result = await KnowledgePanels(facet="category").hunger_game_kp()
    assert result == {
        "HungerGames": {
            "elements": [{"element_type": "text", "text_element": {"html": html}}],
            "title_element": {"title": "Hunger Games (Contribute by playing)"},
        }
    }


async def test_hunger_game_kp_category_with_country():
    """test_hunger_game_kp_category_with_country"""
    html0 = (
        "<ul><li><p><a href='https://hunger.openfoodfacts.org/questions?country=en%3Afrance' "
        "class='button small'><em>Answer questions from Robotoff for the country - France"
        "</em></a></p></li></ul>"
    )
    html1 = (
        "<ul><li><p>"
        "<a href='https://hunger.openfoodfacts.org/questions?country=en%3Afrance&type=category' "
        "class='button small'><em>Answer questions from Robotoff about the category for the"
        " country - France</em></a></p></li></ul>"
    )
    result = await KnowledgePanels(facet="category", country="france").hunger_game_kp()
    assert result == {
        "HungerGames": {
            "elements": [
                {"element_type": "text", "text_element": {"html": html0}},
                {"element_type": "text", "text_element": {"html": html1}},
            ],
            "title_element": {"title": "Hunger Games (Contribute by playing)"},
        }
    }


async def test_hunger_game_kp_category_with_value():
    """test_hunger_game_kp_category_with_value"""
    html = (
        "<ul><li><p><a href='https://hunger.openfoodfacts.org/"
        "questions?type=category&value_tag=en%3Abeers' class='button small'>"
        # noqa: E501
        "<em>Answer questions from Robotoff about the 'en:beers' category</em></a></p></li></ul>"
    )
    result = await KnowledgePanels(facet="category", value="en:beers").hunger_game_kp()
    assert result == {
        "HungerGames": {
            "elements": [{"element_type": "text", "text_element": {"html": html}}],
            "title_element": {"title": "Hunger Games (Contribute by playing)"},
        }
    }


async def test_hunger_game_kp_brand_with_value():
    """test_hunger_game_kp_brand_with_value"""
    html0 = (
        "<ul><li><p><a href='https://hunger.openfoodfacts.org/"
        "questions?type=brand&value_tag=nestle' class='button small'>"
        "<em>Answer questions from Robotoff about the 'nestle' brand</em></a></p></li></ul>"
    )
    html1 = (
        "<ul><li><p><a href='https://hunger.openfoodfacts.org/logos/"
        "deep-search?type=brand&value_tag=nestle' class='button small'>"
        "<em>Annotate the 'nestle' brand more</em></a></p></li></ul>"
    )
    html2 = (
        "<ul><li><p><a href='https://hunger.openfoodfacts.org/logos/product-search?"
        "value_tag=nestle&tagtype=brand' class='button small'>"
        "<em>Kickstart annotation for the 'nestle' brand</em></a></p></li></ul>"
    )
    result = await KnowledgePanels(facet="brand", value="nestle").hunger_game_kp()
    assert result == {
        "HungerGames": {
            "elements": [
                {"element_type": "text", "text_element": {"html": html0}},
                {"element_type": "text", "text_element": {"html": html1}},
                {"element_type": "text", "text_element": {"html": html2}},
            ],
            "title_element": {"title": "Hunger Games (Contribute by playing)"},
        }
    }


async def test_hunger_game_kp_label_with_value():
    """test_hunger_game_kp_label_with_value"""
    html0 = (
        "<ul><li><p><a href='https://hunger.openfoodfacts.org/"
        "questions?type=label&value_tag=en%3Aorganic' class='button small'>"
        "<em>Answer questions from Robotoff about the 'en:organic' label</em></a></p></li></ul>"
    )
    html1 = (
        "<ul><li><p><a href='https://hunger.openfoodfacts.org/logos/deep-search?"
        "type=label&value_tag=en:organic' class='button small'>"
        "<em>Annotate the 'en:organic' label more</em></a></p></li></ul>"
    )
    html2 = (
        "<ul><li><p><a href='https://hunger.openfoodfacts.org/logos/product-search?"
        "value_tag=en:organic&type=label' class='button small'>"
        "<em>Kickstart annotation for the 'en:organic' label</em></a></p></li></ul>"
    )
    result = await KnowledgePanels(facet="label", value="en:organic").hunger_game_kp()
    assert result == {
        "HungerGames": {
            "elements": [
                {"element_type": "text", "text_element": {"html": html0}},
                {"element_type": "text", "text_element": {"html": html1}},
                {"element_type": "text", "text_element": {"html": html2}},
            ],
            "title_element": {"title": "Hunger Games (Contribute by playing)"},
        }
    }


async def test_hunger_game_kp_label_with_value_plural_facet():
    """test_hunger_game_kp_label_with_value_plural_facet"""
    html0 = (
        "<ul><li><p><a href='https://hunger.openfoodfacts.org/"
        "questions?type=label&value_tag=en%3Aorganic' class='button small'>"
        "<em>Answer questions from Robotoff about the 'en:organic' label</em></a></p></li></ul>"
    )
    html1 = (
        "<ul><li><p><a href='https://hunger.openfoodfacts.org/logos/deep-search?"
        "type=label&value_tag=en:organic' class='button small'>"
        "<em>Annotate the 'en:organic' label more</em></a></p></li></ul>"
    )
    html2 = (
        "<ul><li><p><a href='https://hunger.openfoodfacts.org/logos/product-search?"
        "value_tag=en:organic&type=label' class='button small'>"
        "<em>Kickstart annotation for the 'en:organic' label</em></a></p></li></ul>"
    )
    result = await KnowledgePanels(facet="labels", value="en:organic").hunger_game_kp()
    assert result == {
        "HungerGames": {
            "elements": [
                {"element_type": "text", "text_element": {"html": html0}},
                {"element_type": "text", "text_element": {"html": html1}},
                {"element_type": "text", "text_element": {"html": html2}},
            ],
            "title_element": {"title": "Hunger Games (Contribute by playing)"},
        }
    }


async def test_HungerGame_double_country_and_value():
    """test_HungerGame_double_country_and_value"""
    # facet country have priority
    html1 = (
        "<ul><li><p><a href='https://hunger.openfoodfacts.org/questions?country=en%3Afrance' "
        "class='button small'><em>Answer questions from Robotoff for the country - "
        "France</em></a></p></li></ul>"
    )
    html2 = (
        "<ul><li><p><a href='https://hunger.openfoodfacts.org/"
        "questions?country=en%3Afrance&type=category&value_tag=beers' class='button small'>"
        # noqa:E501
        "<em>Answer questions from Robotoff about the 'beers' category for the country - France"
        "</em></a></p></li></ul>"
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
            "title_element": {"title": "Hunger Games (Contribute by playing)"},
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
        "<ul><li><p><a href='https://hunger.openfoodfacts.org/"
        "questions?country=en%3Afrance&brand=lidl' class='button small'>"
        "<em>Answer questions from Robotoff about the 'lidl' brand for the country "
        "- France</em></a></p></li></ul>"
    )
    html1 = (
        "<ul><li><p><a href='https://hunger.openfoodfacts.org/"
        "questions?country=en%3Afrance&brand=lidl&type=category&value_tag=en%3Abeers' "
        "class='button small'><em>Answer questions from Robotoff about the "
        "'en:beers' category and the 'lidl' brand for the country "
        "- France</em></a></p></li></ul>"  # noqa: E501
    )
    html2 = (
        "<ul><li><p><a href='https://hunger.openfoodfacts.org/logos/"
        "deep-search?type=brand&value_tag=lidl' class='button small'>"
        "<em>Annotate the 'lidl' brand more</em></a></p></li></ul>"
    )
    html3 = (
        "<ul><li><p><a href='https://hunger.openfoodfacts.org/logos/"
        "product-search?value_tag=lidl&tagtype=brand' class='button small'>"
        "<em>Kickstart annotation for the 'lidl' brand</em></a></p></li></ul>"
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
                {"element_type": "text", "text_element": {"html": html2}},
                {"element_type": "text", "text_element": {"html": html3}},
            ],
            "title_element": {"title": "Hunger Games (Contribute by playing)"},
        }
    }


async def test_hunger_game_kp_with_all_tag_2():
    """test_hunger_game_kp_with_all_tag_2"""
    html0 = (
        "<ul><li><p><a href='https://hunger.openfoodfacts.org/questions?type=brand' "
        "class='button small'><em>Answer questions from Robotoff about the brand"
        "</em></a></p></li></ul>"
    )
    html1 = (
        "<ul><li><p><a href='https://hunger.openfoodfacts.org/"
        "questions?type=category&value_tag=en%3Acoffees' class='button small'>"
        # noqa: E501
        "<em>Answer questions from Robotoff about the 'en:coffees' category"
        "</em></a></p></li></ul>"
    )
    html2 = (
        "<ul><li><p><a href='https://hunger.openfoodfacts.org/logos/"
        "deep-search?type=brand&value_tag=None' class='button small'>"
        "<em>Annotate the brand more</em></a></p></li></ul>"
    )
    html3 = (
        "<ul><li><p><a href='https://hunger.openfoodfacts.org/logos/"
        "product-search?value_tag=None&tagtype=brand' class='button small'>"
        "<em>Kickstart annotation for the brand</em></a></p></li></ul>"
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
                {"element_type": "text", "text_element": {"html": html2}},
                {"element_type": "text", "text_element": {"html": html3}},
            ],
            "title_element": {"title": "Hunger Games (Contribute by playing)"},
        }
    }


async def test_hunger_game_kp_with_all_tag_3():
    """test_hunger_game_kp_with_all_tag_3"""
    html0 = (
        "<ul><li><p><a href='https://hunger.openfoodfacts.org/questions?country=en%3Aitaly' "
        "class='button small'><em>Answer questions from Robotoff for the country - Italy"
        "</em></a></p></li></ul>"
    )
    html1 = (
        "<ul><li><p><a href='https://hunger.openfoodfacts.org/"
        "questions?country=en%3Aitaly&type=category&value_tag=en%3Ameals' "
        # noqa: E501
        "class='button small'><em>Answer questions from Robotoff about the "
        "'en:meals' category for the country - Italy</em></a></p></li></ul>"
    )
    html2 = (
        "<ul><li><p><a href='https://hunger.openfoodfacts.org/"
        "questions?country=en%3Aitaly&type=label&value_tag=vegan' "
        # noqa: E501
        "class='button small'><em>Answer questions from Robotoff about the 'vegan'"
        " label for the country - Italy</em></a></p></li></ul>"
    )
    html3 = (
        "<ul><li><p><a href='https://hunger.openfoodfacts.org/logos/"
        "deep-search?type=label&value_tag=vegan' class='button small'>"
        "<em>Annotate the 'vegan' label more</em></a></p></li></ul>"
    )
    html4 = (
        "<ul><li><p><a href='https://hunger.openfoodfacts.org/logos/"
        "product-search?value_tag=vegan&type=label' class='button small'>"
        "<em>Kickstart annotation for the 'vegan' label</em></a></p></li></ul>"
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
                {"element_type": "text", "text_element": {"html": html3}},
                {"element_type": "text", "text_element": {"html": html4}},
            ],
            "title_element": {"title": "Hunger Games (Contribute by playing)"},
        }
    }
