import asyncer
import logging
from typing import Union

from fastapi import FastAPI

from .i18n import active_translation
from .knowledge_panels import data_quality_kp, hunger_game_kp, last_edits_kp, wikidata_kp
from .models import FacetName, HungerGameFilter, Taxonomies

app = FastAPI()


@app.get("/")
async def hello():
    return {"message": "Hello from facets-knowledge-panels! Tip: open /docs for documentation"}


@app.get("/knowledge_panel")
async def knowledge_panel(
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
        soon_values = []
        async with asyncer.create_task_group() as task_group:
            if facet_tag in HungerGameFilter.list():
                soon_values.append(
                    task_group.soonify(hunger_game_kp)(
                        hunger_game_filter=facet_tag, value=value_tag, country=country
                    )
                )

            soon_values.append(
                task_group.soonify(data_quality_kp)(
                    facet=facet_tag, value=value_tag, country=country
                )
            )

            soon_values.append(
                task_group.soonify(last_edits_kp)(facet=facet_tag, value=value_tag, country=country)
            )
            if facet_tag in Taxonomies.list():

                soon_values.append(
                    task_group.soonify(wikidata_kp)(facet=facet_tag, value=value_tag)
                )
        panels = []
        for soon_value in soon_values:
            try:
                panels.append(soon_value.value)
            except Exception:
                logging.exception()

        return {"knowledge_panels": panels}
