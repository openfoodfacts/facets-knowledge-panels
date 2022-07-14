from typing import Union

from .models import HungerGameFilter


def hunger_game_kp(hunger_game_filter: HungerGameFilter, value: Union[str, None] = None, country: Union[str, None] = None):
    if country == None and value != None:
        html = f"'<p><a href=\'https://hunger.openfoodfacts.org/?type={hunger_game_filter}&value_tag={value}\'></a></p>\n'"
    elif value == None and country != None:
        html = f"'<p><a href=\'https://hunger.openfoodfacts.org/?type={hunger_game_filter}&country={country}\'></a></p>\n'"
    elif value == None and country == None:
        html = f"'<p><a href=\'https://hunger.openfoodfacts.org/?type={hunger_game_filter}\'></a></p>\n'"
    else:
        html = f"'<p><a href=\'https://hunger.openfoodfacts.org/?type={hunger_game_filter}&value_tag={value}&country={country}\'></a></p>\n'"
    return {
        "hunger-game": {
            "elements": [
                {
                    "element_type": "text",
                    "text_element": {
                        "html": str(html)
                    },
                },
            ],
        },
    }
