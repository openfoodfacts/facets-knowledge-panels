import asyncer
import logging
from typing import Union
from fastapi import FastAPI
from .i18n import active_translation
from .knowledge_panels import data_quality_kp, hunger_game_kp, last_edits_kp
from .models import FacetName, HungerGameFilter

app = FastAPI()


@app.get("/")
async def hello():
    return {
        "message": "Hello from facets-knowledge-panels! Tip: open /docs for documentation"
    }


@app.get("/knowledge_panel")
async def knowledge_panel(
    facet_tag: FacetName,
    value_tag: Union[str, None] = None,
    lang_code: Union[str, None] = None,
    country: Union[str, None] = None,
):
    """
    FacetName is the model that have list of values
    facet_value are the list of values connecting to FacetName eg:- category/beer, here beer is the value
    """
    with active_translation(lang_code):
        async with asyncer.create_task_group() as task_group:
            if facet_tag in HungerGameFilter.list():
                soon_value1 = task_group.soonify(hunger_game_kp)(
                    hunger_game_filter=facet_tag, value=value_tag, country=country
                )

            soon_value2 = task_group.soonify(data_quality_kp)(
                facet=facet_tag, value=value_tag, country=country
            )

            soon_value3 = task_group.soonify(last_edits_kp)(
                facet=facet_tag, value=value_tag, country=country
            )
        panels = []
        try:
            panels.append(soon_value1.value)
        except Exception:
            logging.exception("Hungergame filter doesn't exists")
        try:
            panels.append(soon_value2.value)
        except Exception:
            logging.exception("error occued while appending data_quality_kp")
        try:
            panels.append(soon_value3.value)
        except Exception:
            logging.exception("error occued while appending last_edits_kp")

        return {"knowledge_panels": panels}
