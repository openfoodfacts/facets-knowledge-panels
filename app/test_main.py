from fastapi.testclient import TestClient
import requests
from .main import app

client = TestClient(app)

def ansewer_questions_brand_president():
    response = client.get("/brand/president")
    assert response.status_code == 200
    assert response.json() == {
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

        
def ansewer_questions_brand_president():
    response = client.get("/brand/bad_facet_value")
    assert response.status_code == 404
    assert response.json() == {'detail': 'Not Found'}