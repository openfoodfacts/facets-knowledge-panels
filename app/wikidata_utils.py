from functools import cached_property

import wikidata.client


class WikiDataProperties:
    """some useful properties"""

    @cached_property
    def _client(self):
        return wikidata.client.Client()

    @cached_property
    def image_prop(self):
        return self._client.get("P18")

    @cached_property
    def OSM_prop(self):
        return self._client.get("P402")

    @cached_property
    def INAO_prop(self):
        return self._client.get("P3895")


wikidata_props = WikiDataProperties()


def get_wikidata_entity(entity_id: str):
    client = wikidata.client.Client()
    return client.get(entity_id)
