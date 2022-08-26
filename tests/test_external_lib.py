from collections import namedtuple
import wikidata.client

Entities = namedtuple(
    "Entities",
    [
        "label_tag",
        "description_tag",
        "image_url",
    ],
)


def getwikidata():
    client = wikidata.client.Client
    return client.get("Q47472153")


def test_client(monkeypatch):
    def mock_get(entity_id):
        assert entity_id == "Q47472153"
        entity = Entities(
            "chicken sausage",
            "type of sausage",
            "https://upload.wikimedia.org/wikipedia/commons/0/0d/Chicken_sausages_-_Tapa.JPG",
        )
        return entity

    monkeypatch.setattr(
        wikidata.client.Client,
        "get",
        mock_get,
    )

    x = getwikidata()
    assert x == Entities(
        label_tag="chicken sausage",
        description_tag="type of sausage",
        image_url="https://upload.wikimedia.org/wikipedia/commons/0/0d/Chicken_sausages_-_Tapa.JPG",
    )
