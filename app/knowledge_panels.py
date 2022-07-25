import json
from typing import Union
from urllib.parse import urlencode

import requests

from .models import HungerGameFilter, country_to_ISO_code, facet_plural


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


def last_edits_kp(
    facet: str,
    value: Union[str, None] = None,
    country: Union[str, None] = None,
):
    if facet == "packaging":
        plural = facet
    else:
        plural = facet_plural(facet=facet)
    query = {
        "fields": "code,last_editor,last_modified_t",
        "sort_by": "last_modified_t",
    }
    if facet == "country":
        country_code = country_to_ISO_code(value=value)
        country = value
        url = f"https://{country_code}-en.openfoodfacts.org"
        description = f"{value}"
    else:
        if value is not None:
            url = "https://world.openfoodfacts.org"
            query[f"{plural}_tags_en"] = value
            description = f"{value} based for {facet}"
        if country is not None:
            country_code = country_to_ISO_code(value=country)
            url = f"https://{country_code}-en.openfoodfacts.org"
            description = f"{facet} based for {country}"

    search_url = f"{url}/api/v2/search"
    description = f"last-edits issues related to {description}"
    response_API = requests.get(search_url, params=query)
    data = response_API.json()
    counts = data["count"]
    tags = data["products"]
    html = "\n".join(
        f'<li>Product with this code {tag["code"]} was last edited by {tag["last_editor"]} has last_modified_tag {tag["last_modified_t"]}</li>'
        for tag in tags[0:10]
    )
    html = f"<ul>{html}</ul>"

    return {
        "last-edits": {
            "elements": [
                {
                    "element_type": "text",
                    "counts": counts,
                    "text_element": html,
                    "total_edits": counts,
                    "source_url": f"{url}/{facet}/{value}?sort_by=last_modified_t",
                    "description": f"This is {description}",
                },
            ],
        },
    }
