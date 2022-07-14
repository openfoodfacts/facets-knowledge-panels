from typing import Union

from urllib.parse import urlencode

from .models import HungerGameFilter


def hunger_game_kp(
    hunger_game_filter: HungerGameFilter,
    value: Union[str, None] = None,
    country: Union[str, None] = None,
):
    baseUrl = "https://hunger.openfoodfacts.org/?type="
    valueQuery = urlencode({"value_tag": value})
    countryQuery = urlencode({"country": country})
    if country == None and value != None:
        html = f"<p><a href='{baseUrl}{hunger_game_filter}&{valueQuery}'></a></p>\n'"
    elif value == None and country != None:
        html = f"<p><a href='{baseUrl}{hunger_game_filter}&{countryQuery}'></a></p>\n'"
    elif value == None and country == None:
        html = f"<p><a href='{baseUrl}{hunger_game_filter}'></a></p>\n'"
    else:
        html = f"<p><a href='{baseUrl}{hunger_game_filter}&{valueQuery}&{countryQuery}'></a></p>\n'"
    return {
        "hunger-game": {
            "elements": [
                {
                    "element_type": "text",
                    "text_element": {"html": str(html)},
                },
            ],
        },
    }
