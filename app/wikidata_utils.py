import wikidata.client


def get_wikidata(entity_id=str):
    client = wikidata.client.Client()
    entity = client.get(entity_id)
    description_tag = entity.description["en"]
    label_tag = entity.label["en"]
    image_prop = client.get("P18")
    # Open Street map releation
    OSM_prop = client.get("P402")
    # INAO poduct releation
    INAO_prop = client.get("P3895")
    return entity, description_tag, label_tag, image_prop, OSM_prop, INAO_prop
