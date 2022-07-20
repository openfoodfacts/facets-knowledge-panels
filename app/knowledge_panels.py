import json
from typing import Union
from urllib.parse import urlencode

import requests

from .models import HungerGameFilter


def hunger_game_kp(
    hunger_game_filter: HungerGameFilter,
    value: Union[str, None] = None,
    country: Union[str, None] = None,
):
    query = {}
    description = ""
    if hunger_game_filter == "country":
        country = value
        hunger_game_filter = value = None
    if country is not None:
        query["country"] = country
        description = country
    if hunger_game_filter is not None:
        query["type"] = f"{hunger_game_filter}"
        description = f"{hunger_game_filter}"
    if value is not None:
        query["value_tag"] = value
        description = f"{value} {hunger_game_filter}"
    questions_url = "https://hunger.openfoodfacts.org/questions"
    if query:
        questions_url += f"?{urlencode(query)}"
    description = f"Answer robotoff questions about {description}"
    html = f"<p><a href='{questions_url}'>{description}</a></p>\n"
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


def kp_taxonomy_data(facet: str, value: str):

    query = {}
    if value is not None:
        query["tagtype"] = facet
        query[
            "fields"
        ] = "name,parents,children,wikidata,auth_url,country_code_2,language_codes,country_code_3,e_number,additives_classes"
        query["tags"] = value
    search_url = "https://world.openfoodfacts.org/api/v2/taxonomy"
    if query:
        search_url += f"?{urlencode(query)}"

    response_API = requests.get(search_url)
    data = response_API.text
    parse_json = json.loads(data)
    return parse_json
