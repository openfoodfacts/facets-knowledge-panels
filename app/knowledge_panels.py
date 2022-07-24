import json
from typing import Union
from urllib.parse import urlencode, urljoin

import requests

from .models import HungerGameFilter, country_to_ISO_code


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
        country_code = country_to_ISO_code(value=value)
        country = value
        url = f"https://{country_code}-en.openfoodfacts.org"
        path = None
        description = f"{value}"
    else:
        if country is not None:
            country_code = country_to_ISO_code(value=country)
            url = f"https://{country_code}-en.openfoodfacts.org/"
            path = f"{facet}/{value}"
            description = f"{facet} based for {country}"
        else:
            url = "https://world.openfoodfacts.org/"
            path = f"{facet}/{value}"
            description = f"{value} based for {facet}"
    source_url = urljoin(url, path)
    description = f"data-quality issues related to {description}"
    quality_url = f"{source_url}/data-quality.json"
    """
        Parsing data from the url
        """
    response_API = requests.get(quality_url)
    data = response_API.json()
    total_issues = data["count"]
    # Returns total number of issues
    tags = data["tags"]
    html = "\n".join(
        f'<li><a href="{tag["url"]}">{tag["products"]} products with {tag["name"]}</a></li>'
        for tag in tags[0:3]
    )
    html = f"<ul>{html}</ul>"
    return {
        "data-quality": {
            "elements": [
                {
                    "element_type": "text",
                    "total_issues": total_issues,
                    "text_element": html,
                }
            ],
            "source_url": f"{source_url}/data-quality",
            "description": f"This is a {description}",
        },
    }
