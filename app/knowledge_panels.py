from typing import Union
import json
import requests

from urllib.parse import urlencode, urljoin

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


def data_quality_kp(
    facet,
    value: Union[str, None] = None,
    country: Union[str, None] = None,
):
    if facet == "country":
        path = f"{facet}/{value}"
        description = "country"
    else:
        if country is not None:
            path = f"country/{country}/{facet}/{value}"
            description = f"{facet} based on {country}"
        else:
            path = f"{facet}/{value}"
            description = facet
    url = "https://world.openfoodfacts.org/"
    source_url = urljoin(url, path)
    description = f"data-quality issues releated to this {description}"
    html = f"{source_url}/data-quality.json"
    response_API = requests.get(html)
    data = response_API.text
    parse_json = json.loads(data)
    numbers_of_issues = parse_json["count"]
    tags = parse_json["tags"]
    first_three_data = tags[0:3]

    return {
        "data-quality": {
            "elements": [
                {
                    "element_type": "text",
                    "total_issues": numbers_of_issues,
                    "text_element": first_three_data,
                    "source_url": html,
                    "description": description,
                },
            ],
        },
    }
