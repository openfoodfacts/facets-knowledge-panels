import logging
from typing import Union

from fastapi import FastAPI

from .i18n import active_translation
from .knowledge_panels import KnowledgePanels
from .models import FacetName, HungerGameFilter, Taxonomies

app = FastAPI()


@app.get("/")
def hello():
    return {"message": "Hello from facets-knowledge-panels! Tip: open /docs for documentation"}


@app.get("/knowledge_panel")
def knowledge_panel(
    facet_tag: str,
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
            facet=facet_tag,
            value=value_tag,
            sec_facet=sec_facet_tag,
            sec_value=sec_value_tag,
            country=country,
        )
        try:
            if facet_tag in HungerGameFilter:
                panels.append(obj_kp.hunger_game_kp())
        except Exception:
            logging.exception("error occued while appending data-quality-kp")
        try:
            panels.append(obj_kp.data_quality_kp())
        except Exception:
            logging.exception("error occued while appending data-quality-kp")
        try:
            panels.append(obj_kp.last_edits_kp())
        except Exception:
            logging.exception("error occued while appending data-quality-kp")
        try:
            panels.append(obj_kp.wikidata_kp())
        except Exception:
            logging.exception("error occued while appending data-quality-kp")

        return {"knowledge_panels": panels}
