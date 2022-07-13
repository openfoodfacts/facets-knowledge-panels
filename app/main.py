from typing import Union

from fastapi import FastAPI

from .knowledge_panels import hunger_game_kp
from .models import Facetname, Hunger_game_filter

app = FastAPI()


@app.get("/")
def hello():
    return {"message": "Hello from facets-knowledge-panels! Tip: open /docs for documentation"}


@app.get("/knowledge_panel")
def knowledge_panel(facet_name: Facetname, facet_value: Union[str, None] = None, country: Union[str, None] = None):

    panels = []
    if facet_name in Hunger_game_filter.list():
        panels.append(hunger_game_kp(hunger_game_filter=facet_name,
                      value=facet_value, country=country))
    else:
        panels.append(
            "Sorry! hunger game knowlege panel for this facet isn't available right now")

    return {"knowledge_panels": panels}
