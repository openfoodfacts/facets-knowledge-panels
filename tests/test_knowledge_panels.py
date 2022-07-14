from app.main import hunger_game_kp


def test_hunger_game_kp_with_category():
    assert hunger_game_kp(hunger_game_filter="catergory") == {'hunger-game': {'elements': [{'element_type': 'text', 'text_element': {
        'html': "'<p><a href='https://hunger.openfoodfacts.org/?type=catergory'></a></p>\n'"}}]}}


def test_hunger_game_kp_category_with_country():
    assert hunger_game_kp(hunger_game_filter="catergory", country="france") == {'hunger-game': {'elements': [{'element_type': 'text', 'text_element': {
        'html': "'<p><a href='https://hunger.openfoodfacts.org/?type=catergory&country=france'></a></p>\n'"}}]}}


def test_hunger_game_kp_category_with_value():
    assert hunger_game_kp(hunger_game_filter="catergory", value="beer") == {'hunger-game': {'elements': [{'element_type': 'text', 'text_element': {
        'html': "'<p><a href='https://hunger.openfoodfacts.org/?type=catergory&value_tag=beer'></a></p>\n'"}}]}}


def test_hunger_game_kp_with_brand():
    assert hunger_game_kp(hunger_game_filter="brand") == {'hunger-game': {'elements': [{'element_type': 'text', 'text_element': {
        'html': "'<p><a href='https://hunger.openfoodfacts.org/?type=brand'></a></p>\n'"}}]}}


def test_hunger_game_kp_brand_with_country():
    assert hunger_game_kp(hunger_game_filter="brand", country="India") == {'hunger-game': {'elements': [{'element_type': 'text', 'text_element': {
        'html': "'<p><a href='https://hunger.openfoodfacts.org/?type=brand&country=India'></a></p>\n'"}}]}}


def test_hunger_game_kp_brand_with_value():
    assert hunger_game_kp(hunger_game_filter="brand", value="nestle") == {'hunger-game': {'elements': [{'element_type': 'text', 'text_element': {
        'html': "'<p><a href='https://hunger.openfoodfacts.org/?type=brand&value_tag=nestle'></a></p>\n'"}}]}}


def test_hunger_game_kp_with_label():
    assert hunger_game_kp(hunger_game_filter="label") == {'hunger-game': {'elements': [{'element_type': 'text', 'text_element': {
        'html': "'<p><a href='https://hunger.openfoodfacts.org/?type=label'></a></p>\n'"}}]}}


def test_hunger_game_kp_label_with_country():
    assert hunger_game_kp(hunger_game_filter="label", country="Italy") == {'hunger-game': {'elements': [{'element_type': 'text', 'text_element': {
        'html': "'<p><a href='https://hunger.openfoodfacts.org/?type=label&country=Italy'></a></p>\n'"}}]}}


def test_hunger_game_kp_label_with_value():
    assert hunger_game_kp(hunger_game_filter="label", value="organic") == {'hunger-game': {'elements': [{'element_type': 'text', 'text_element': {
        'html': "'<p><a href='https://hunger.openfoodfacts.org/?type=label&value_tag=organic'></a></p>\n'"}}]}}
