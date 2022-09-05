import logging
from typing import Union

from fastapi import FastAPI

from .i18n import active_translation
from .knowledge_panels import data_quality_kp, hunger_game_kp, last_edits_kp, wikidata_kp
from .models import FacetName, FacetResponse, HungerGameFilter, Taxonomies


tags_metadata = [
    {
        "name": "knowledge-panel",
        "description": "Return different knowledge panels based on the facet provided.",
    },
]
description = """
Providing knowledge panels for a particular Open Food Facts facet (category, brand, etc...)

A standardized way for clients to get semi-structured but generic data that they can present to users on product pages.
"""

app = FastAPI(
    title="Open Food Facts knowledge Panels API",
    description=description,
    version="0.0.1",
    contact={
        "name": "Slack",
        "url": "https://openfoodfacts.slack.com/archives/C03LFRKLVBQ",
    },
    license_info={
        "name": "GNU Affero General Public License v3.0",
        "url": "https://www.gnu.org/licenses/agpl-3.0.en.html",
    },
    openapi_tags=tags_metadata,
)


@app.get("/")
def hello():
    return {"message": "Hello from facets-knowledge-panels! Tip: open /docs for documentation"}


@app.get("/knowledge_panel", tags=["knowledge-panel"], response_model=FacetResponse)
def knowledge_panel(
    facet_tag: FacetName,
    value_tag: Union[str, None] = None,
    lang_code: Union[str, None] = None,
    country: Union[str, None] = None,
):
    """
    FacetName is the model that have list of values
    facet_tag are the list of values connecting to FacetName
    eg:- category/beer, here beer is the value
    """
    with active_translation(lang_code):
        panels = []
        if facet_tag in HungerGameFilter.list():
            panels.append(
                hunger_game_kp(hunger_game_filter=facet_tag, value=value_tag, country=country)
            )
        try:
            panels.append(data_quality_kp(facet=facet_tag, value=value_tag, country=country))
        except Exception:
            logging.exception("error occued while appending data-quality-kp")
        try:
            panels.append(last_edits_kp(facet=facet_tag, value=value_tag, country=country))
        except Exception:
            logging.exception("error occued while appending last-edits-kp")
        try:
            if facet_tag in Taxonomies.list():
                panels.append(wikidata_kp(facet=facet_tag, value=value_tag))
        except Exception:
            logging.exception("error occurred while appending wikidata-kp")

        return {"knowledge_panels": panels}
