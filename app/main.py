import logging
import re
from contextlib import asynccontextmanager
from typing import Annotated, List, Optional, Union

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
        "name": "health-check",
        "description": "Health check and API status endpoints",
        "externalDocs": {
            "description": "Learn more about API health checks",
            "url": "https://github.com/openfoodfacts/facets-knowledge-panels"
        }
    },
    {
        "name": "knowledge-panels",
        "description": "Knowledge panels for Open Food Facts facets - Get structured information about categories, brands, and other facets",
        "externalDocs": {
            "description": "Knowledge Panels Documentation",
            "url": "https://openfoodfacts.github.io/openfoodfacts-server/api/explain-knowledge-panels/"
        }
    },
    {
        "name": "html-rendering",
        "description": "HTML rendering services for knowledge panels - Convert knowledge panels to HTML format",
        "externalDocs": {
            "description": "HTML Rendering Guide",
            "url": "https://github.com/openfoodfacts/facets-knowledge-panels/blob/main/template/item.html"
        }
    },
]
description = """
## Open Food Facts Knowledge Panels API

Providing **knowledge panels** for Open Food Facts facets (categories, brands, labels, etc.)

### What are Knowledge Panels?

Knowledge panels are **contextual information widgets** that provide:
- **Data quality insights** and improvement suggestions
- **Gamified contribution** links (Hunger Games)
- **External knowledge** from Wikidata and other sources
- **Recent activity** and edit history

### Why Use This API?

- **Standardized format**: Consistent data structure for all facets
- **Contextual information**: Relevant data for specific categories, brands, etc.
- **Contribution opportunities**: Help users find ways to improve data quality
- **Multi-language support**: Localized content in multiple languages
- **Flexible integration**: JSON API with optional HTML rendering

### How to Use

1. **Choose a facet type**: category, brand, label, packaging, etc.
2. **Specify the value**: e.g., 'en:beers', 'coca-cola', 'organic'
3. **Optionally filter**: by language, country, or specific panels
4. **Get structured data**: Use for web apps, mobile apps, or direct display

### Examples

- **Categories**: `/knowledge_panel?facet_tag=category&value_tag=en:beers`
- **Brands**: `/knowledge_panel?facet_tag=brand&value_tag=coca-cola`
- **Labels**: `/knowledge_panel?facet_tag=label&value_tag=organic&lang_code=fr`

### Contributing

You can contribute at https://github.com/openfoodfacts/facets-knowledge-panels

For more information about knowledge panels, see the [conceptual overview](https://openfoodfacts.github.io/openfoodfacts-server/api/explain-knowledge-panels/).
"""  # noqa: E501

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await start_global_quality_refresh()
    yield
    # Shutdown
    ...


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
    lifespan=lifespan,
    servers=[
        {
            "url": "https://facets-kp.openfoodfacts.org",
            "description": "Production server"
        },
        {
            "url": "http://127.0.0.1:8000",
            "description": "Local development server"
        },
        {
            "url": "http://localhost:8000",
            "description": "Local development server (localhost)"
        }
    ]
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


@repeat_every(seconds=3 * 60 * 60, logger=logger, wait_first=True)
async def start_global_quality_refresh():
    # Clearing cache and refetching data-quality
    # Refetching data every hour
    await global_quality_refresh()


@app.get(
    "/",
    tags=["health-check"],
    summary="API Health Check",
    description="Get the API status and basic information. Use this endpoint to verify that the API is running correctly.",
    response_description="API status message with a tip about accessing the documentation"
)
async def hello():
    return {"message": "Hello from facets-knowledge-panels! Tip: open /docs for documentation"}


@app.get(
    "/knowledge_panel", 
    tags=["knowledge-panels"], 
    response_model=FacetResponse,
    summary="Get Knowledge Panels for Facets",
    description="""
    Get knowledge panels for Open Food Facts facets like categories, brands, labels, etc.
    
    **Knowledge panels provide contextual information** such as:
    - Data quality issues and suggestions for improvement
    - Links to Hunger Games (gamified data entry)
    - Wikidata information and external links
    - Recent edits and activity
    
    **Example usage:**
    - `facet_tag=category&value_tag=en:beers` - Get panels for beer category
    - `facet_tag=brand&value_tag=coca-cola` - Get panels for Coca-Cola brand
    - `facet_tag=label&value_tag=organic` - Get panels for organic label
    
    You can include/exclude specific panels and filter by language and country.
    """,
    response_description="Knowledge panels data including structured information panels"
)
async def knowledge_panel(
    request: Request,
    facet_tag: str = QueryData.facet_tag_query(),
    value_tag: Optional[str] = QueryData.value_tag_query(),
    sec_facet_tag: Optional[str] = QueryData.secondary_facet_tag_query(),
    sec_value_tag: Optional[str] = QueryData.secondary_value_tag_query(),
    lang_code: Optional[str] = QueryData.language_code_query(),
    country: Optional[str] = QueryData.country_query(),
    include: Annotated[Union[List[PanelName], None], QueryData.include_panel_query()] = None,
    exclude: Annotated[Union[List[PanelName], None], QueryData.exclude_panel_query()] = None,
):
    """
    Get knowledge panels for a specific Open Food Facts facet.
    
    A facet represents a classification dimension in the Open Food Facts database:
    - **facet_tag**: The type of classification (e.g., 'category', 'brand', 'label')
    - **value_tag**: The specific value within that classification (e.g., 'en:beers', 'coca-cola', 'organic')
    
    The response includes various knowledge panels that provide contextual information
    to help users understand and contribute to data quality for that facet.
    
    **Panel Types:**
    - `hunger_game`: Links to gamified data entry tasks
    - `data_quality`: Information about data completeness and quality issues
    - `wikidata`: External knowledge from Wikidata
    - `last_edits`: Recent activity and edits
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


@app.get(
    "/render-to-html", 
    tags=["html-rendering"], 
    response_class=HTMLResponse,
    summary="Render Knowledge Panels as HTML",
    description="""
    Render knowledge panels as HTML using Jinja2 templates.
    
    This endpoint takes the same parameters as `/knowledge_panel` but returns
    the result as formatted HTML instead of JSON. This is useful for:
    
    - **Direct embedding** in web applications
    - **Server-side rendering** scenarios  
    - **Integration with Open Food Facts server** for product pages
    
    The HTML is generated using the `item.html` template and includes
    all the styling and structure needed to display knowledge panels.
    
    **Use cases:**
    - Embedding panels directly in product pages
    - Server-side rendering for better SEO
    - Integration with existing HTML-based interfaces
    """,
    response_description="Formatted HTML containing the rendered knowledge panels"
)
async def render_html(
    request: Request,
    facet_tag: str = QueryData.facet_tag_query(),
    value_tag: Optional[str] = QueryData.value_tag_query(),
    sec_facet_tag: Optional[str] = QueryData.secondary_facet_tag_query(),
    sec_value_tag: Optional[str] = QueryData.secondary_value_tag_query(),
    lang_code: Optional[str] = QueryData.language_code_query(),
    country: Optional[str] = QueryData.country_query(),
    include: Annotated[Union[List[PanelName], None], QueryData.include_panel_query()] = None,
    exclude: Annotated[Union[List[PanelName], None], QueryData.exclude_panel_query()] = None,
):
    """
    Render knowledge panels as HTML using Jinja2 templates.
    
    This is a helper function that makes it easier to inject facet knowledge panels
    into the Open Food Facts server or other HTML-based applications.
    
    The function internally calls the knowledge_panel endpoint and then renders
    the results using the item.html template with proper styling and structure.
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
