from typing import Union

from fastapi import FastAPI

from .models import Facetname, Hunger_game_filter

app = FastAPI()


@app.get("/")
def hello():
    return {"message": "Hello from facets-knowledge-panels! Tip: open /docs for documentation"}


@app.get("/hunger-game-kp")
def knowledge_panel_hunger_game(hunger_game_filter: Hunger_game_filter, value: Union[str, None] = None, country: Union[str, None] = None):
    html = f"'<p><a href=\'https://hunger.openfoodfacts.org/?type={hunger_game_filter}&value_tag={value}&country={country}\'></a></p>\n'"
    return {
        "knowledge_panels": [
            {
                "hunger-game": {
                    "elements": [
                        {
                            "element_type": "text",
                            "text_element": {
                                "html": str(html)
                            },
                        },
                    ],
                },

            },
        ],
    }


@app.get("/{facet_name}/{facet_value}")
def knowledge_panel(facet_name: Facetname, facet_value: str):
    return {"knowledge_panels": []}
