import logging
import re
from typing import Annotated, Optional

import asyncer
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi_utils.tasks import repeat_every
from prometheus_fastapi_instrumentator import Instrumentator

from .i18n import active_translation
from .knowledge_panels import KnowledgePanels
from .models import FacetResponse, PanelName, QueryData
from .off import global_quality_refresh

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

A standardized way for clients to get semi-structured but generic data that they can present
to users on product pages.
You can contribute at https://github.com/openfoodfacts/facets-knowledge-panels
You should also read https://openfoodfacts.github.io/openfoodfacts-server/api/explain-knowledge-panels/
for the Product Page knowledge panels which follow the same syntax (the docs provides a conceptual overview).
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

app.add_middleware(
    CORSMiddleware,
    # FastAPI doc related to allow_origin (to avoid CORS issues):
    # "It's also possible to declare the list as "*" (a "wildcard") to say that all are allowed.
    # This will exclude credentials (cookies, authorization headers, etc.)
    # which is fine for us
    # If in the future you want to use allow-credentials, use `allow_origin_regex`
    # see: https://github.com/tiangolo/fastapi/issues/133#issuecomment-646985050
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

Instrumentator(should_respect_env_var=True, env_var_name="FACETS_ENABLE_METRICS").instrument(
    app
).expose(app)


logger = logging.getLogger(__name__ + ".global_taxonomy_refresh")


CRAWL_BOT_RE = re.compile(
    r"Googlebot|Googlebot-Image|bingbot|Applebot|YandexBot|"
    r"YandexRenderResourcesBot|DuckDuckBot|DotBot|SeekportBot|AhrefsBot|"
    r"DataForSeoBot|SeznamBot|ZoomBot|MojeekBot|QRbot|www\.qwant\.com|"
    r"facebookexternalhit|Bytespider|GPTBot|SEOkicks-Robot|SearchmetricsBot"
    r"MJ12bot|SurveyBot|SEOdiver|wotbox|Cliqzbot|Paracrawl|VelenPublicWebCrawler"
    r"SemrushBot|MegaIndex\.ru|YandexMarket|Amazonbot"
)


def is_crawling_bot(request: Request):
    """Return True if the client is a web crawler, based on User-Agent header."""
    user_agent = request.headers.get("User-Agent", "")
    return CRAWL_BOT_RE.search(user_agent) is not None


@app.on_event("startup")
@repeat_every(seconds=3 * 60 * 60, logger=logger, wait_first=True)
async def start_global_quality_refresh():
    # Clearing cache and refetching data-quality
    # Refetching data every hour
    await global_quality_refresh()


@app.get("/")
async def hello():
    return {"message": "Hello from facets-knowledge-panels! Tip: open /docs for documentation"}


@app.get("/knowledge_panel", tags=["knowledge-panel"], response_model=FacetResponse)
async def knowledge_panel(
    request: Request,
    facet_tag: str = QueryData.facet_tag_query(),
    value_tag: Optional[str] = QueryData.value_tag_query(),
    sec_facet_tag: Optional[str] = QueryData.secondary_facet_tag_query(),
    sec_value_tag: Optional[str] = QueryData.secondary_value_tag_query(),
    lang_code: Optional[str] = QueryData.language_code_query(),
    country: Optional[str] = QueryData.country_query(),
    include: Annotated[list[PanelName] | None, QueryData.include_panel_query()] = None,
    exclude: Annotated[list[PanelName] | None, QueryData.exclude_panel_query()] = None,
):
    """
    FacetName is the model that have list of values
    facet_tag are the list of values connecting to FacetName
    eg:- category/beer, here beer is the value
    """
    if include is not None and exclude is not None:
        raise HTTPException(status_code=400, detail="include and exclude parameters are exclusive")

    panel_names = {PanelName.hunger_game, PanelName.wikidata}
    if include is not None:
        panel_names = set(include)
    elif exclude is not None:
        panel_names -= set(exclude)

    if is_crawling_bot(request):
        # Don't return any knowledge panel if the client is a crawling bot
        return {"knowledge_panels": {}}

    with active_translation(lang_code):
        # creating object that will compute knowledge panels
        obj_kp = KnowledgePanels(
            facet=facet_tag,
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
            if PanelName.hunger_game in panel_names:
                soon_panels.append(task_group.soonify(obj_kp.hunger_game_kp)())
            if PanelName.data_quality in panel_names:
                soon_panels.append(task_group.soonify(obj_kp.data_quality_kp)())
            if PanelName.last_edits in panel_names:
                soon_panels.append(task_group.soonify(obj_kp.last_edits_kp)())
            if PanelName.wikidata in panel_names:
                soon_panels.append(task_group.soonify(obj_kp.wikidata_kp)())
        # collect panels results
        panels = {}
        for soon_value in soon_panels:
            # Appending soon_value value in panels
            # as soon_panels needs to access outside taskgroup.
            if soon_value.value:
                panels.update(soon_value.value)
        return {"knowledge_panels": panels}


templates = Jinja2Templates(directory="template")


@app.get("/render-to-html", tags=["Render to HTML"], response_class=HTMLResponse)
async def render_html(
    request: Request,
    facet_tag: str = QueryData.facet_tag_query(),
    value_tag: Optional[str] = QueryData.value_tag_query(),
    sec_facet_tag: Optional[str] = QueryData.secondary_facet_tag_query(),
    sec_value_tag: Optional[str] = QueryData.secondary_value_tag_query(),
    lang_code: Optional[str] = QueryData.language_code_query(),
    country: Optional[str] = QueryData.country_query(),
    include: Annotated[list[PanelName] | None, QueryData.include_panel_query()] = None,
    exclude: Annotated[list[PanelName] | None, QueryData.exclude_panel_query()] = None,
):
    """
    Render item.html using jinja2
    This is helper function to make thing easier while injecting facet_kp in off-server
    """
    panels = await knowledge_panel(
        request,
        facet_tag,
        value_tag,
        sec_facet_tag,
        sec_value_tag,
        lang_code,
        country,
        include,
        exclude,
    )
    return templates.TemplateResponse("item.html", {"request": request, "panels": panels})
