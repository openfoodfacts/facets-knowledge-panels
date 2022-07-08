from typing import Union

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def hello():
    return {"message": "Hello from facets-knowledge-panels! Tip: open /docs for documentation"}

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

