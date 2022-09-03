from typing import Union
from urllib.parse import urlencode

from .models import HungerGameFilter, country_to_ISO_code, facet_plural
from .off import data_quality, hungergame, last_edit, wikidata_helper


def hunger_game_kp(
    hunger_game_filter: HungerGameFilter,
    value: Union[str, None] = None,
    sec_facet: Union[str, None] = None,
    sec_value: Union[str, None] = None,
    country: Union[str, None] = None,
):
    query = {}
    description = ""
    if hunger_game_filter == "country":
        country = value
        hunger_game_filter = value = None
    if country is not None:
        query["country"] = f"en:{country}"
        description = country
    if hunger_game_filter is not None:
        # Making primary facet as sec and vise versa
        if hunger_game_filter == "brand":
            query["brand"] = value
            description = f"brand {value}"
            if sec_value is not None:
                query["type"] = f"{sec_facet}"
                query["value_tag"] = sec_value
                description += f" {sec_facet} {sec_value}"
        else:
            query["type"] = f"{hunger_game_filter}"
            description = f"{hunger_game_filter}"
            if value is not None:
                query["value_tag"] = value
                description = f"{hunger_game_filter} {value}"
            if sec_facet == "brand":
                query[sec_facet] = sec_value
                description += f" {sec_facet} {sec_value}"
    questions_url = "https://hunger.openfoodfacts.org/questions"
    if query:
        questions_url += f"?{urlencode(query)}"
    t_description = hungergame()
    description = f"{t_description} {description}"
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
    sec_facet: Union[str, None] = None,
    sec_value: Union[str, None] = None,
    country: Union[str, None] = None,
):
    """
    Get data corresponding to differnet facet
    """
    path = ""
    description = ""
    if facet == "country":
        country = value
        country_code = country_to_ISO_code(value=value)
        url = f"https://{country_code}-en.openfoodfacts.org"
        path = ""
        facet = value = None
    if country is not None:
        country_code = country_to_ISO_code(value=country)
        url = f"https://{country_code}-en.openfoodfacts.org"
        path = ""
        description += f"{country} "
    if country is None:
        url = "https://world.openfoodfacts.org/"
    if facet is not None:
        path += facet
        description += f"{facet}"
    if value is not None:
        path += f"/{value}"
        description += f" {value}"
    # Checking if secondary facet is provided
    if sec_facet is not None:
        path += f"/{sec_facet}"
        description += f" {sec_facet}"
    if sec_value is not None:
        path += f"/{sec_value}"
        description += f" {sec_value}"
    (quality_html, source_url, t_description, t_title) = data_quality(url=url, path=path)

    return {
        "Quality": {
            "title": t_title,
            "subtitle": f"{t_description} {description}",
            "source_url": f"{source_url}/data-quality",
            "elements": [
                {
                    "element_type": "text",
                    "text_element": quality_html,
                }
            ],
        },
    }


def last_edits_kp(
    facet: str,
    value: Union[str, None] = None,
    sec_facet: Union[str, None] = None,
    sec_value: Union[str, None] = None,
    country: Union[str, None] = None,
):
    """
    Return knowledge panel for last-edits corresponding to different facet
    """
    query = {
        "fields": "product_name,code,last_editor,last_edit_dates_tags",
        "sort_by": "last_modified_t",
    }
    description = ""
    if facet == "country":
        country = value
        country_code = country_to_ISO_code(value=value)
        url = f"https://{country_code}-en.openfoodfacts.org"
        facet = value = None
    if country is not None:
        country_code = country_to_ISO_code(value=country)
        url = f"https://{country_code}-en.openfoodfacts.org"
        description += f"{country} "
    if country is None:
        url = "https://world.openfoodfacts.org"
    if facet is not None:
        description += f"{facet}"
    if value is not None:
        query[f"{facet_plural(facet=facet)}_tags_en"] = value
        description += f" {value}"
        source_url = f"{url}/{facet}/{value}?sort_by=last_modified_t"
    if sec_value is not None:
        query[f"{facet_plural(facet=sec_facet)}_tags_en"] = sec_value
        description += f" {sec_facet} {sec_value}"
        source_url = f"{url}/{facet}/{value}/{sec_facet}/{sec_value}?sort_by=last_modified_t"
    expected_html, t_description, t_title = last_edit(url=url, query=query)

    return {
        "LastEdits": {
            "title": t_title,
            "subtitle": f"{t_description} {description}",
            "source_url": source_url,
            "elements": [
                {
                    "element_type": "text",
                    "text_element": expected_html,
                },
            ],
        },
    }


def wikidata_kp(facet: str, value: str):
    """
    Return knowledge panel for wikidata
    """
    query = {}
    if value:
        query["tagtype"] = facet_plural(facet=facet)
        query["fields"] = "wikidata"
        query["tags"] = value

    entities = wikidata_helper(query=query, value=value)
    return {
        "WikiData": {
            "title": "wiki-data",
            "subtitle": entities.description_tag,
            "source_url": f"https://www.wikidata.org/wiki/{entities.entity_id}",
            "elements": [
                {
                    "element_type": "text",
                    "text_element": entities.label_tag,
                    "image_url": entities.image_url,
                },
                {
                    "element_type": "links",
                    "wikipedia": entities.wikipedia_relation,
                    "open_street_map": entities.OSM_relation,
                    "INAO": entities.INAO_relation,
                },
            ],
        },
    }
