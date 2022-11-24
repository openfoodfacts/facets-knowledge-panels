import urllib
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


def image_thumbnail(image_url: str, width: int):
    """
    tries to build image thumbnail for wikimedia image
    """
    # only for pattern we know
    url = urllib.parse.urlparse(image_url)
    if url.path.startswith("/wikipedia/commons/"):
        # add components to get thumbnail
        dirs = url.path.split("/")
        dirs.insert(3, "thumb")
        dirs.append(f"{width}px-thumbnail.jpg")
        url = url._replace(path="/".join(dirs))
    return url.geturl()
