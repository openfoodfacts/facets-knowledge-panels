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
        description = f"{value}"
    else:
        if country is not None:
            path = f"country/{country}/{facet}/{value}"
            description = f"{facet} based for {country}"
        else:
            path = f"{facet}/{value}"
            description = f"{value} based for {facet}"
    url = "https://world.openfoodfacts.org/"
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
    first_three = tags[0:3]
    # Returns First three issues sorted by most common
    id = []
    name = []
    products = []
    known = []
    url = []
    for i in first_three:
        id.append(i["id"])
        name.append(i["name"])
        products.append(i["products"])
        known.append(i["known"])
        url.append(i["url"])
    # Fetching data from first_three(sorted first three data)
    if len(first_three) == 3:
        return {
            "data-quality": {
                "elements": [
                    {
                        "element_type": "text",
                        "total_issues": total_issues,
                        "text_element_1": {
                            "id": id[0],
                            "title": name[0],
                            "known": known[0],
                            "poducts": products[0],
                            "html": f'<a href="{url[0]}"></a>.',
                        },
                        "text_element_2": {
                            "id": id[1],
                            "title": name[1],
                            "known": known[1],
                            "poducts": products[1],
                            "html": f'<a href="{url[1]}"></a>.',
                        },
                        "text_element_3": {
                            "id": id[2],
                            "title": name[2],
                            "known": known[2],
                            "poducts": products[2],
                            "html": f'<a href="{url[2]}"></a>.',
                        },
                    }
                ],
                "source_url": f"{source_url}/data-quality",
                "description": f"This is a {description}",
            },
        }
    elif len(first_three) == 0:
        return {
            "data-quality": {
                "elements": [
                    {
                        "element_type": "text",
                        "total_issues": total_issues,
                        "text_element_1": {},
                    }
                ],
                "source_url": f"{source_url}/data-quality",
                "description": f"This is a {description}",
            },
        }
    elif len(first_three) == 1:
        return {
            "data-quality": {
                "elements": [
                    {
                        "element_type": "text",
                        "total_issues": total_issues,
                        "text_element_1": {
                            "id": id[0],
                            "title": name[0],
                            "known": known[0],
                            "poducts": products[0],
                            "html": f'<a href="{url[0]}"></a>.',
                        },
                    }
                ],
                "source_url": f"{source_url}/data-quality",
                "description": f"This is a {description}",
            },
        }
    elif len(first_three) == 2:
        return {
            "data-quality": {
                "elements": [
                    {
                        "element_type": "text",
                        "total_issues": total_issues,
                        "text_element_1": {
                            "id": id[0],
                            "title": name[0],
                            "known": known[0],
                            "poducts": products[0],
                            "html": f'<a href="{url[0]}"></a>.',
                        },
                        "text_element_2": {
                            "id": id[1],
                            "title": name[1],
                            "known": known[1],
                            "poducts": products[1],
                            "html": f'<a href="{url[1]}"></a>.',
                        },
                    }
                ],
                "source_url": f"{source_url}/data-quality",
                "description": f"This is a {description}",
            },
        }
