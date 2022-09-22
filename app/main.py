import logging
from typing import Union

import asyncer
from fastapi import FastAPI

from .i18n import active_translation
from .knowledge_panels import KnowledgePanels
from .models import FacetName, FacetResponse, HungerGameFilter, Taxonomies

# Metadata for the API
tags_metadata = [
    {
        "name": "knowledge-panel",
        "description": "Return different knowledge panels based on the facet provided.",
    },
]
description = """
Providing knowledge panels for a particular Open Food Facts facet (category, brand, etc...)

A standardized way for clients to get semi-structured but generic data that they can present to users on product pages.
"""  # noqa: E501

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
async def hello():
    return {"message": "Hello from facets-knowledge-panels! Tip: open /docs for documentation"}


@app.get("/knowledge_panel", response_model=FacetResponse)
async def knowledge_panel(
    facet_tag: FacetName,
    value_tag: Union[str, None] = None,
    sec_facet_tag: Union[str, None] = None,
    sec_value_tag: Union[str, None] = None,
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
        # creating object that will compute knowledge panels
        obj_kp = KnowledgePanels(
            facet=facet_tag.value,
            value=value_tag,
            sec_facet=sec_facet_tag,
            sec_value=sec_value_tag,
            country=country,
        )
        # this will contains panels computations
        soon_panels = []
        # the task_group will run these knowledge_panels async functions concurrently
        async with asyncer.create_task_group() as task_group:
            # launch each panels computation
            if facet_tag in HungerGameFilter.list():
                soon_panels.append(task_group.soonify(obj_kp.hunger_game_kp)())
            soon_panels.append(task_group.soonify(obj_kp.data_quality_kp)())
            soon_panels.append(task_group.soonify(obj_kp.last_edits_kp)())
            if facet_tag in Taxonomies.list():
                soon_panels.append(task_group.soonify(obj_kp.wikidata_kp)())
        # collect panels results
        for soon_value in soon_panels:
            # if an exception was raised during computation
            # we will get it on value retrieval
            # but we don't want to sacrifice whole result for a single failure
            # as most panels depends on external resources that may not be available
            try:
                panels.append(soon_value.value)
            except Exception:
                logging.exception()

        return {"knowledge_panels": panels}
