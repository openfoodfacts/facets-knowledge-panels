import logging
from typing import Union

from fastapi import FastAPI

from .i18n import active_translation
from .knowledge_panels import data_quality_kp, hunger_game_kp, last_edits_kp
from .models import FacetName, HungerGameFilter

app = FastAPI()


@app.get("/")
def hello():
    return {
        "message": "Hello from facets-knowledge-panels! Tip: open /docs for documentation"
    }


@app.get("/knowledge_panel")
def knowledge_panel(
    facet_tag: FacetName,
    value_tag: Union[str, None] = None,
    sec_facet_tag: Union[str, None] = None,
    sec_value_tag: Union[str, None] = None,
    lang_code: Union[str, None] = None,
    country: Union[str, None] = None,
):
    """
    FacetName is the model that have list of values
    facet_value are the list of values connecting to FacetName eg:- category/beer, here beer is the value
    """
    with active_translation(lang_code):
        panels = []
        if facet_tag in HungerGameFilter.list():
            panels.append(
                hunger_game_kp(
                    hunger_game_filter=facet_tag, value=value_tag, country=country
                )
            )
        try:
            panels.append(
                data_quality_kp(
                    facet=facet_tag,
                    value=value_tag,
                    sec_facet=sec_facet_tag,
                    sec_value=sec_value_tag,
                    country=country,
                )
            )
        except Exception:
            logging.exception("error occued while appending data-quality-kp")
        try:
            panels.append(
                last_edits_kp(
                    facet=facet_tag,
                    value=value_tag,
                    sec_facet=sec_facet_tag,
                    sec_value=sec_value_tag,
                    country=country,
                )
            )
        except Exception:
            logging.exception("error occued while appending last-edits-kp")

        return {"knowledge_panels": panels}
