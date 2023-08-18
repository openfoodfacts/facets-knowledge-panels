import logging
import re
from typing import Annotated

import asyncer
from aiofile import async_open
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi_utils.tasks import repeat_every
from openfoodfacts.types import Country, Lang
from prometheus_fastapi_instrumentator import Instrumentator

from app.information_kp import find_kp_html_path
from app.settings import HTML_DIR

from .i18n import DEFAULT_LANGUAGE, active_translation
from .knowledge_panels import KnowledgePanels
from .models import (
    COUNTRY_QUERY,
    FACET_TAG_QUERY,
    LANGUAGE_CODE_QUERY,
    SECONDARY_FACET_TAG_QUERY,
    SECONDARY_VALUE_TAG_QUERY,
    VALUE_TAG_QUERY,
    FacetResponse,
)
from .off import global_quality_refresh
from .utils import secure_filename, singularize

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
    r"facebookexternalhit"
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
    facet_tag: Annotated[str, FACET_TAG_QUERY],
    value_tag: Annotated[str | None, VALUE_TAG_QUERY] = None,
    sec_facet_tag: Annotated[str | None, SECONDARY_FACET_TAG_QUERY] = None,
    sec_value_tag: Annotated[str | None, SECONDARY_VALUE_TAG_QUERY] = None,
    lang_code: Annotated[Lang, LANGUAGE_CODE_QUERY] = Lang[DEFAULT_LANGUAGE],
    country: Annotated[Country, COUNTRY_QUERY] = Country.world,
    add_contribution_panels: bool = True,
    add_information_panels: bool = True,
):
    """Return knowledge panels for a `facet_tag` and an optional `facet_value`.
    `sec_facet_tag` and `sec_value_tag` are used when accessing nested facets
    on Open Food Facts website.

    This endpoint returns 2 types of knowledge panels (controlled by
    `add_contribution_panels` and `add_information_panels` flags respectively):

    - contribution knowledge panels: knowledge panels useful for contributors (Hunger
      Game links, last edits,...)
    - information knowledge panel: description of the category/label...

    Information knowledge panels are country-specific and language-specific.
    If no knowledge panel was found for the requested country, Country.world is
    used as a fallback.

    This mechanism allows for example to have a different knowledge panel for `en:organic`
    in France and in the USA (where we will mostly talk about en:usda-organic) label.
    """
    panels = {}
    facet_tag = singularize(facet_tag)
    sec_facet_tag = singularize(sec_facet_tag)

    if not is_crawling_bot(request) and add_contribution_panels:
        # Don't return any knowledge panel if the client is a crawling bot
        with active_translation(lang_code.value):
            # creating object that will compute knowledge panels

            obj_kp = KnowledgePanels(
                facet=facet_tag,
                value=value_tag,
                sec_facet=sec_facet_tag,
                sec_value=sec_value_tag,
                country=country.value if country is not Country.world else None,
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
            for soon_value in soon_panels:
                # Appending soon_value value in panels
                # as soon_panels needs to access outside taskgroup.
                if soon_value.value:
                    panels.update(soon_value.value)

    if add_information_panels and value_tag is not None:
        # As we're using user-provided data to access filesystem,
        # generate secure filename
        facet_tag_safe = secure_filename(facet_tag)
        value_tag_safe = secure_filename(value_tag)

        if facet_tag_safe and value_tag_safe:
            file_path = find_kp_html_path(
                HTML_DIR, facet_tag_safe, value_tag_safe, country, lang_code
            )
            panel = None
            if file_path is not None:
                async with async_open(file_path, "r") as f:
                    html_content = await f.read()
                panel = {
                    "elements": [{"element_type": "text", "text_element": {"html": html_content}}],
                    "title_element": {"title": "Description"},
                }
                panels["Description"] = panel

    return {"knowledge_panels": panels}


templates = Jinja2Templates(directory="template", trim_blocks=True, lstrip_blocks=True)


@app.get("/render-to-html", tags=["Render to HTML"], response_class=HTMLResponse)
async def render_html(
    request: Request,
    facet_tag: Annotated[str, FACET_TAG_QUERY],
    value_tag: Annotated[str | None, VALUE_TAG_QUERY] = None,
    sec_facet_tag: Annotated[str | None, SECONDARY_FACET_TAG_QUERY] = None,
    sec_value_tag: Annotated[str | None, SECONDARY_VALUE_TAG_QUERY] = None,
    lang_code: Annotated[Lang, LANGUAGE_CODE_QUERY] = Lang[DEFAULT_LANGUAGE],
    country: Annotated[Country, COUNTRY_QUERY] = Country.world,
    add_contribution_panels: bool = True,
    add_information_panels: bool = True,
):
    """
    Render item.html using jinja2
    This is helper function to make thing easier while injecting facet_kp in off-server
    """
    panels = await knowledge_panel(
        request=request,
        facet_tag=facet_tag,
        value_tag=value_tag,
        sec_facet_tag=sec_facet_tag,
        sec_value_tag=sec_value_tag,
        lang_code=lang_code,
        country=country,
        add_contribution_panels=add_contribution_panels,
        add_information_panels=add_information_panels,
    )
    return templates.TemplateResponse("item.html", {"request": request, "panels": panels})
