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


def last_edits_kp(facet: str, value: str):
    list = ["country", "category"]
    if facet in list:
        word = facet[:-1]
        pural_facet = word + "ies"
    elif facet == "packaging":
        pural_facet = facet
    else:
        pural_facet = facet + "s"
    """
    Changing facet to pural because that how the search api works
    """
    query = {}
    if value is not None:
        query[f"{pural_facet}_tags_en"] = value
        query["fields"] = "code,product_name,last_editor"
        query["sort_by"] = "last_modified_t"
    search_url = "https://world.openfoodfacts.org/api/v2/search"
    if query:
        search_url += f"?{urlencode(query)}"

    response_API = requests.get(search_url)
    data = response_API.text
    parse_json = json.loads(data)
    counts = parse_json["count"]
    tags = parse_json["products"]
    first_three = tags[0:3]
    """Parsing data """

    return {
        "last-edits": {
            "elements": [
                {
                    "element_type": "text",
                    "total_issues": counts,
                    "text_element": first_three,
                    "source_url": search_url,
                },
            ],
        },
    }
