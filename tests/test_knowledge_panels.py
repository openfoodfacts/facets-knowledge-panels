from app.main import hunger_game_kp, data_quality_kp


def test_hunger_game_kp_with_filter_value_and_country():
    assert hunger_game_kp(
        hunger_game_filter="country", value="germany", country="france"
    ) == {
        "hunger-game": {
            "elements": [
                {
                    "element_type": "text",
                    "text_element": {
                        "html": "<p><a href='https://hunger.openfoodfacts.org/questions?country=germany'>Answer robotoff questions about germany</a></p>\n"
                    },
                }
            ]
        }
    }


def test_hunger_game_kp_with_category():
    assert hunger_game_kp(hunger_game_filter="category") == {
        "hunger-game": {
            "elements": [
                {
                    "element_type": "text",
                    "text_element": {
                        "html": "<p><a href='https://hunger.openfoodfacts.org/questions?type=category'>Answer robotoff questions about category</a></p>\n"
                    },
                }
            ]
        }
    }


def test_hunger_game_kp_category_with_country():
    assert hunger_game_kp(hunger_game_filter="category", country="france") == {
        "hunger-game": {
            "elements": [
                {
                    "element_type": "text",
                    "text_element": {
                        "html": "<p><a href='https://hunger.openfoodfacts.org/questions?country=france&type=category'>Answer robotoff questions about category</a></p>\n"
                    },
                }
            ]
        }
    }


def test_hunger_game_kp_category_with_value():
    assert hunger_game_kp(hunger_game_filter="category", value="beer") == {
        "hunger-game": {
            "elements": [
                {
                    "element_type": "text",
                    "text_element": {
                        "html": "<p><a href='https://hunger.openfoodfacts.org/questions?type=category&value_tag=beer'>Answer robotoff questions about beer category</a></p>\n"
                    },
                }
            ]
        }
    }


def test_hunger_game_kp_brand_with_value():
    assert hunger_game_kp(hunger_game_filter="brand", value="nestle") == {
        "hunger-game": {
            "elements": [
                {
                    "element_type": "text",
                    "text_element": {
                        "html": "<p><a href='https://hunger.openfoodfacts.org/questions?type=brand&value_tag=nestle'>Answer robotoff questions about nestle brand</a></p>\n"
                    },
                }
            ]
        }
    }


def test_hunger_game_kp_label_with_value():
    assert hunger_game_kp(hunger_game_filter="label", value="organic") == {
        "hunger-game": {
            "elements": [
                {
                    "element_type": "text",
                    "text_element": {
                        "html": "<p><a href='https://hunger.openfoodfacts.org/questions?type=label&value_tag=organic'>Answer robotoff questions about organic label</a></p>\n"
                    },
                }
            ]
        }
    }


def test_data_quality_kp_with_country_and_facet():
    assert data_quality_kp(
        facet="packaging", value="plastic-box", country="Hungary"
    ) == {
        "data-quality": {
            "elements": [
                {
                    "element_type": "text",
                    "total_issues": 0,
                    "text_element": [],
                    "source_url": "https://world.openfoodfacts.org/country/Hungary/packaging/plastic-box/data-quality.json",
                    "description": "data-quality issues related to packaging based for Hungary",
                }
            ]
        }
    }


def test_data_quality_kp_with_country_only():
    assert data_quality_kp(facet="country", value="united kingdom") == {
        "data-quality": {
            "elements": [
                {
                    "element_type": "text",
                    "total_issues": 241,
                    "text_element": [
                        {
                            "id": "en:ecoscore-production-system-no-label",
                            "known": 0,
                            "name": "ecoscore-production-system-no-label",
                            "products": 74495,
                            "url": "https://world.openfoodfacts.org/country/united-kingdom/data-quality/ecoscore-production-system-no-label",
                        },
                        {
                            "id": "en:ecoscore-origins-of-ingredients-origins-are-100-percent-unknown",
                            "known": 0,
                            "name": "ecoscore-origins-of-ingredients-origins-are-100-percent-unknown",
                            "products": 73475,
                            "url": "https://world.openfoodfacts.org/country/united-kingdom/data-quality/ecoscore-origins-of-ingredients-origins-are-100-percent-unknown",
                        },
                        {
                            "id": "en:ecoscore-threatened-species-ingredients-missing",
                            "known": 0,
                            "name": "ecoscore-threatened-species-ingredients-missing",
                            "products": 57632,
                            "url": "https://world.openfoodfacts.org/country/united-kingdom/data-quality/ecoscore-threatened-species-ingredients-missing",
                        },
                    ],
                    "source_url": "https://world.openfoodfacts.org/country/united kingdom/data-quality.json",
                    "description": "data-quality issues related to united kingdom",
                }
            ]
        }
    }
