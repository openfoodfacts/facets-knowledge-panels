import logging
from typing import Optional

import asyncer
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from prometheus_fastapi_instrumentator import Instrumentator

from .i18n import active_translation
from .knowledge_panels import KnowledgePanels
from .models import FacetName, FacetResponse, QueryData

# Metadata for the API
tags_metadata = [
    {
        "name": "knowledge-panel",
        "description": "Return different knowledge panels based on the facet provided.",
    },
    {
        "name": "Render to HTML",
        "description": "Render html based on knowledge panels.",
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


@app.on_event("startup")
async def start_prometheus_metrics():
    """setup metrics on startup"""
    # condition instrumentation by FACETS_ENABLE_METRICS
    Instrumentator(should_respect_env_var=True, env_var_name="FACETS_ENABLE_METRICS").instrument(
        app
    ).expose(app)


@app.get("/")
async def hello():
    return {"message": "Hello from facets-knowledge-panels! Tip: open /docs for documentation"}


@app.get("/knowledge_panel", tags=["knowledge-panel"], response_model=FacetResponse)
async def knowledge_panel(
    facet_tag: FacetName = QueryData.facet_tag_query(),
    value_tag: Optional[str] = QueryData.value_tag_query(),
    sec_facet_tag: Optional[str] = QueryData.secondary_facet_tag_query(),
    sec_value_tag: Optional[str] = QueryData.secondary_value_tag_query(),
    lang_code: Optional[str] = QueryData.language_code_query(),
    country: Optional[str] = QueryData.country_query(),
):
    """
    FacetName is the model that have list of values
    facet_tag are the list of values connecting to FacetName
    eg:- category/beer, here beer is the value
    """
    if facet_tag == "country" and value_tag is None:
        raise HTTPException(status_code=400, detail="Value_tag can't be empty!")
    with active_translation(lang_code):
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
            soon_panels.append(task_group.soonify(obj_kp.hunger_game_kp)())
            soon_panels.append(task_group.soonify(obj_kp.data_quality_kp)())
            soon_panels.append(task_group.soonify(obj_kp.last_edits_kp)())
            soon_panels.append(task_group.soonify(obj_kp.wikidata_kp)())
        # collect panels results
        panels = {}
        for soon_value in soon_panels:
            # if an exception was raised during computation
            # we will get it on value retrieval
            # but we don't want to sacrifice whole result for a single failure
            # as most panels depends on external resources that may not be available
            try:
                if soon_value.value:
                    panels.update(soon_value.value)
            except Exception:
                logging.exception()
        return {"knowledge_panels": panels}


templates = Jinja2Templates(directory="template")


@app.get("/render-to-html", tags=["Render to HTML"], response_class=HTMLResponse)
async def render_html(
    request: Request,
    facet_tag: FacetName = QueryData.facet_tag_query(),
    value_tag: Optional[str] = QueryData.value_tag_query(),
    sec_facet_tag: Optional[str] = QueryData.secondary_facet_tag_query(),
    sec_value_tag: Optional[str] = QueryData.secondary_value_tag_query(),
    lang_code: Optional[str] = QueryData.language_code_query(),
    country: Optional[str] = QueryData.country_query(),
):
    """
    Render item.html using jinja2
    """
    panels = await knowledge_panel(
        facet_tag,
        value_tag,
        sec_facet_tag,
        sec_value_tag,
        country,
        lang_code,
    )
    return templates.TemplateResponse("item.html", {"request": request, "panels": panels})
