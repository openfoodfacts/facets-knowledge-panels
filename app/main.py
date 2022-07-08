from typing import Union
from fastapi import FastAPI
from .models import Facetname, Facetvalue

app = FastAPI()

@app.get("/brand/president")

def ansewer_questions_brand_president():
    return {
            "knowledge_panels": [
                {
                    "hunger-game": {
                        "type": "hunger-game",
                        "level": "questions",
                        "elements": [
                            {
                            "element_type": "text",
                            "text_element": {
                                "html":"<p><a href=\"https://hunger.openfoodfacts.org/?type=brand&value_tag=president\">Answer questions about brand president</a></p>\n"
                            },
                            },
                        ],
                    },
                            
                },
            ],
        }

@app.get("/{facet_name}/{facet_value}")
def knowledge_panel(facet_name :Facetname,facet_value: Facetvalue ):
    return { "knowledge_panels": []}

