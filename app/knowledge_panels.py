from typing import Union
from urllib.parse import urlencode

from .models import country_to_ISO_code, facet_plural
from .off import data_quality, hungergame, last_edit, wikidata_helper


class KnowledgePanels:
    def __init__(self, facet, value, sec_facet, sec_value, country):
        self.facet = facet
        self.value = value
        self.sec_facet = sec_facet
        self.sec_value = sec_value
        self.country = country

    def hunger_game_kp(self):
        query = {}
        questions_url = "https://hunger.openfoodfacts.org/questions"
        facets = {self.facet: self.value, self.sec_facet: self.sec_value}
        filtered = {k: v for k, v in facets.items() if k is not None}
        facets.clear()
        facets.update(filtered)
        urls = set()
        html = []
        if self.country is not None:
            query["country"] = f"en:{self.country}"
        if "country" in facets.keys():
            facet_value = facets.get("country")
            query["country"] = f"en:{facet_value}"
            facets.pop("country")
        if "brand" in facets.keys():
            facet_value = facets.get("brand")
            if facet_value is not None:
                query["brand"] = facet_value
            else:
                query["type"] = "brand"
            facets.pop("brand")
        for k, v in facets.items():
            query["type"] = k
            if v is not None:
                query["value"] = v
            urls.add(questions_url + f"?{urlencode(query)}")
        if len(facets) != 2:
            questions_url += f"?{urlencode(query)}"
            urls.add(questions_url)
        t_description = hungergame()
        for id, val in enumerate(urls):
            html.append(
                {
                    "id": id,
                    "element_type": "text",
                    "text_element": {"html": f"<p><a href='{val}'>{t_description}</a></p>"},
                },
            )

        kp = {"hunger-game": {"title": "hunger-games", "elements": html}}

        return kp

    def data_quality_kp(self):
        """
        Get data corresponding to differnet facet
        """
        path = ""
        description = ""
        if self.facet == "country":
            self.country = self.value
            country_code = country_to_ISO_code(value=self.value)
            url = f"https://{country_code}-en.openfoodfacts.org"
            path = ""
            self.facet = self.value = None
        if self.country is not None:
            country_code = country_to_ISO_code(value=self.country)
            url = f"https://{country_code}-en.openfoodfacts.org"
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
        (quality_html, source_url, t_description, t_title) = data_quality(url=url, path=path)

        return {
            "Quality": {
                "title": t_title,
                "subtitle": f"{t_description} {description}",
                "source_url": f"{source_url}/data-quality",
                "elements": [
                    {
                        "element_type": "text",
                        "text_element": quality_html,
                    }
                ],
            },
        }

    def last_edits_kp(self):
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
            url = f"https://{country_code}-en.openfoodfacts.org"
            self.facet = self.value = None
        if self.country is not None:
            country_code = country_to_ISO_code(value=self.country)
            url = f"https://{country_code}-en.openfoodfacts.org"
            description += f"{self.country} "
        if self.country is None:
            url = "https://world.openfoodfacts.org"
        if self.facet is not None:
            description += f"{self.facet}"
        if self.value is not None:
            query[f"{facet_plural(facet=self.facet)}_tags_en"] = self.value
            description += f" {self.value}"
            source_url = f"{url}/{self.facet}/{self.value}?sort_by=last_modified_t"
        if self.sec_value is not None:
            query[f"{facet_plural(facet=self.sec_facet)}_tags_en"] = self.sec_value
            description += f" {self.sec_facet} {self.sec_value}"
            source_url = f"{url}/{self.facet}/{self.value}/{self.sec_facet}/{self.sec_value}?sort_by=last_modified_t"
        expected_html, t_description, t_title = last_edit(url=url, query=query)

        return {
            "LastEdits": {
                "title": t_title,
                "subtitle": f"{t_description} {description}",
                "source_url": source_url,
                "elements": [
                    {
                        "element_type": "text",
                        "text_element": expected_html,
                    },
                ],
            },
        }

    def wikidata_kp(self):
        """
        Return knowledge panel for wikidata
        """
        query = {}
        if self.value:
            query["tagtype"] = facet_plural(facet=self.facet)
            query["fields"] = "wikidata"
            query["tags"] = self.value

        entities = wikidata_helper(query=query, value=self.value)
        return {
            "WikiData": {
                "title": "wiki-data",
                "subtitle": entities.description_tag,
                "source_url": f"https://www.wikidata.org/wiki/{entities.entity_id}",
                "elements": [
                    {
                        "element_type": "text",
                        "text_element": entities.label_tag,
                        "image_url": entities.image_url,
                    },
                    {
                        "element_type": "links",
                        "wikipedia": entities.wikipedia_relation,
                        "open_street_map": entities.OSM_relation,
                        "INAO": entities.INAO_relation,
                    },
                ],
            },
        }
