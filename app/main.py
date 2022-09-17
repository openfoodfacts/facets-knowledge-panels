import asyncer
import logging
from typing import Union

from fastapi import FastAPI

from .i18n import active_translation
from .knowledge_panels import KnowledgePanels
from .models import FacetName, HungerGameFilter

app = FastAPI()


@app.get("/")
async def hello():
    return {"message": "Hello from facets-knowledge-panels! Tip: open /docs for documentation"}


@app.get("/knowledge_panel")
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
        obj_kp = KnowledgePanels(
            facet=facet_tag.value,
            value=value_tag,
            sec_facet=sec_facet_tag,
            sec_value=sec_value_tag,
            country=country,
        )
        try:
            if facet_tag in HungerGameFilter.list():
                panels.append(await obj_kp.hunger_game_kp())
        except Exception:
            logging.exception("error occued while appending hungergames-kp")
        try:
            panels.append(await obj_kp.data_quality_kp())
        except Exception:
            logging.exception("error occued while appending data-quality-kp")
        try:
            panels.append(await obj_kp.last_edits_kp())
        except Exception:
            logging.exception("error occued while appending last-edites-kp")
        try:
            panels.append(await obj_kp.wikidata_kp())
        except Exception:
            logging.exception("error occued while appending wikidata-kp")

        return {"knowledge_panels": panels}
