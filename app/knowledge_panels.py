import logging
from typing import Union
from urllib.parse import urlencode

from .models import country_to_ISO_code, facet_plural
from .off import data_quality, hungergame, last_edit, wikidata_helper


class KnowledgePanels:
    def __init__(
        self,
        facet: str,
        value: Union[str, None] = None,
        sec_facet: Union[str, None] = None,
        sec_value: Union[str, None] = None,
        country: Union[str, None] = None,
    ):
        self.facet = facet
        self.value = value
        self.sec_facet = sec_facet
        self.sec_value = sec_value
        self.country = country

    async def hunger_game_kp(self):
        query = {}
        questions_url = "https://hunger.openfoodfacts.org/questions"
        facets = {self.facet: self.value, self.sec_facet: self.sec_value}
        filtered = {k: v for k, v in facets.items() if k is not None}
        facets.clear()
        facets.update(filtered)
        urls = set()
        description = ""
        html = []
        if self.country is not None:
            query["country"] = f"en:{self.country}"
            description = f"for country {self.country}"
        if facets.get("country"):
            country_value = facets.pop("country")
            query["country"] = f"en:{country_value}"
            description = f"{country_value}"
        if facets.get("brand") and len(facets) > 1:
            brand_value = facets.pop("brand")
            query["brand"] = brand_value
            description += f" for brand {brand_value}"
        # generate an url for each remaining facets
        for k, v in facets.items():
            value_description = ""
            facet_query = dict(query)
            facet_query["type"] = k
            facet_description = k
            if v is not None:
                facet_query["value_tag"] = v
                value_description += v
            urls.add(
                (
                    f"{questions_url}?{urlencode(facet_query)}",
                    f"{facet_description} {value_description} {description}".strip(),
                )
            )
        if query:
            urls.add((f"{questions_url}?{urlencode(query)}", description))

        t_description = await hungergame()
        for id, val in enumerate(sorted(urls)):
            url, des = val
            html.append(
                {
                    "element_type": "text",
                    "text_element": {"html": f"<p><a href='{url}'>{t_description} {des}</a></p>"},
                },
            )

        kp = {"hunger_game": {"elements": html, "title_element": {"title": "hunger-games"}}}

        return kp

    async def data_quality_kp(self):
        """
        Get data corresponding to differnet facet
        """
        path = ""
        description = ""
        if self.facet == "country":
            self.country = self.value
            country_code = country_to_ISO_code(value=self.value)
            url = f"https://{country_code}.openfoodfacts.org"
            path = ""
            self.facet = self.value = None
        if self.sec_facet == "country":
            self.country = self.sec_value
            country_code = country_to_ISO_code(value=self.sec_value)
            url = f"https://{country_code}.openfoodfacts.org"
            path = ""
            self.sec_facet = self.sec_value = None
        if self.country is not None:
            country_code = country_to_ISO_code(value=self.country)
            url = f"https://{country_code}.openfoodfacts.org"
            path = ""
            description += f"{self.country} "
        if self.country is None:
            url = "https://world.openfoodfacts.org/"
        if self.facet is not None:
            path += self.facet
            description += f"{self.facet}"
        if self.value is not None:
            path += f"/{self.value}"
            description += f" {self.value}"
        # Checking if secondary facet is provided
        if self.sec_facet is not None:
            path += f"/{self.sec_facet}"
            description += f" {self.sec_facet}"
        if self.sec_value is not None:
            path += f"/{self.sec_value}"
            description += f" {self.sec_value}"
        (t_html, source_url, t_description, t_title) = await data_quality(url=url, path=path)

        return {
            "Quality": {
                "elements": [
                    {
                        "element_type": "text",
                        "text_element": {
                            "html": t_html,
                            "source_text": t_title,
                            "source_url": f"{source_url}/data-quality",
                        },
                    }
                ],
                "title_element": {"title": f"{t_description} {description}"},
            },
        }

    async def last_edits_kp(self):
        """
        Return knowledge panel for last-edits corresponding to different facet
        """
        query = {
            "fields": "product_name,code,last_editor,last_edit_dates_tags",
            "sort_by": "last_modified_t",
        }
        description = ""
        if self.facet == "country":
            self.country = self.value
            country_code = country_to_ISO_code(value=self.value)
            url = f"https://{country_code}.openfoodfacts.org"
            self.facet = self.value = None
        if self.sec_facet == "country":
            self.country = self.sec_value
            country_code = country_to_ISO_code(value=self.sec_value)
            url = f"https://{country_code}.openfoodfacts.org"
            self.sec_facet = self.sec_value = None
        if self.country is not None:
            country_code = country_to_ISO_code(value=self.country)
            url = f"https://{country_code}.openfoodfacts.org"
            description += f"{self.country} "
        if self.country is None:
            url = "https://world.openfoodfacts.org"
        if self.facet is not None:
            description += f"{self.facet}"
            source_url = f"{url}/{self.facet}?sort_by=last_modified_t"
        if self.value is not None:
            query[f"{facet_plural(facet=self.facet)}_tags_en"] = self.value
            description += f" {self.value}"
            source_url = f"{url}/{self.facet}/{self.value}?sort_by=last_modified_t"
        if self.sec_value and self.sec_facet is not None:
            query[f"{facet_plural(facet=self.sec_facet)}_tags_en"] = self.sec_value
            description += f" {self.sec_facet} {self.sec_value}"
            source_url = f"{url}/{self.facet}/{self.value}/{self.sec_facet}/{self.sec_value}?sort_by=last_modified_t"  # noqa: E501
        t_html, t_description, t_title = await last_edit(url=url, query=query)

        return {
            "LastEdits": {
                "elements": [
                    {
                        "element_type": "text",
                        "text_element": {
                            "html": t_html,
                            "source_text": t_title,
                            "source_url": source_url,
                        },
                    },
                ],
                "title_element": {"title": f"{t_description} {description}"},
            },
        }

    async def _wikidata_kp(self, facet, value):
        query = {}
        if value:
            query["tagtype"] = facet_plural(facet=facet)
            query["fields"] = "wikidata"
            query["tags"] = value

        entities = await wikidata_helper(query=query, value=value)

        return entities

    async def wikidata_kp(self):
        """
        Return knowledge panel for wikidata
        """
        entities = set()
        try:
            entities.add(await self._wikidata_kp(facet=self.facet, value=self.value))
        except Exception:
            logging.exception("While adding wikidata for primary facet")
        try:
            entities.add(await self._wikidata_kp(facet=self.sec_facet, value=self.sec_value))
        except Exception:
            logging.exception("While adding wikidata for secandary facet")

        html = []
        for id, val in enumerate(entities):
            html.append(
                {
                    "element_type": "text",
                    "text_element": {
                        "source_label": val.label_tag,
                        "source_description": val.description_tag,
                        "source_text": "wikidata",
                        "source_url": f"https://www.wikidata.org/wiki/{val.entity_id}",
                    },
                }
            )

            html.append(
                {
                    "element_type": "links",
                    "link_element": {
                        "wikipedia": val.wikipedia_relation,
                        "image_url": val.image_url,
                        "open_street_map": val.OSM_relation,
                        "INAO": val.INAO_relation,
                    },
                }
            )

        return {
            "WikiData": {"elements": html, "title_element": {"title": "wikidata"}},
        }
