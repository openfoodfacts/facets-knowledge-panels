import collections
from typing import Optional, Union
from urllib.parse import urlencode

from .config import openFoodFacts, settings
from .exception_wrapper import no_exception
from .i18n import translate as _
from .models import (
    HungerGameQuestionFilter,
    HungerGameLogoFilter,
    Taxonomies,
    alpha2_to_country_name,
    country_name_to_alpha2,
    pluralize,
    singularize,
)
from .off import data_quality, last_edit, wikidata_helper
from .utils import wrap_text, format_translation


class KnowledgePanels:
    def __init__(
        self,
        facet: str,
        value: Union[str, None] = None,
        sec_facet: Union[str, None] = None,
        sec_value: Union[str, None] = None,
        country: Union[str, None] = None,
    ):
        self.facet = singularize(facet)
        self.value = value
        self.sec_facet = singularize(sec_facet)
        self.sec_value = sec_value
        self.country = alpha2_to_country_name(country)

    async def hunger_game_kp(self) -> Optional[dict]:
        query = {}
        questions_url = settings().HUNGER_GAME + "/questions"
        facets = {self.facet: self.value, self.sec_facet: self.sec_value}
        # remove empty values and facets that are not hunger games related
        facets_logo = {
            k: v for k, v in facets.items() if k is not None and k in HungerGameLogoFilter.list()
        }
        facets = {k: v for k, v in facets.items() if k is not None and k in HungerGameQuestionFilter.list()}
        urls = set()
        descriptions = collections.OrderedDict()
        description_values = dict()
        html = []
        # a country is specified
        if self.country is not None:
            query["country"] = f"en:{self.country}"
            descriptions["country"] = "for the country - {country}"
            description_values["country"] = self.country.capitalize()

        # one of the facet is a country, use it as a country parameter
        if facets.get("country"):
            country_value = facets.pop("country")
            # remove eventual prefix
            country_value = country_value.split(":", 1)[-1]
            query["country"] = f"en:{country_value}"
            descriptions["country"] = "for the country - {country}"
            description_values["country"] = country_value.capitalize()

        # brand can be used as a filter, if we have more than one facet
        if facets.get("brand") and len(facets) > 1:
            brand_value = facets.pop("brand")
            query["brand"] = brand_value
            descriptions["brand"] = "and the {brand_name} brand"
            description_values["brand_name"] = wrap_text(brand_value, "single_quotes")

        if descriptions.get("country"):
            descriptions.move_to_end(
                "country"
            )  # so that 'for the country - <country name>' is always at the end.
        description = " ".join(descriptions.values())
        # generate an url for each remaining facets
        for k, v in facets.items():
            value_description = ""
            facet_query = dict(query)
            facet_query["type"] = k
            facet_description = k
            if v is not None:
                facet_query["value_tag"] = v
                value_description += wrap_text(v, "single_quotes")
            if value_description:
                value_description += " "
            urls.add(
                (
                    f"{questions_url}?{urlencode(facet_query)}",
                    f"about the {{facet_value}}{{facet_name}} {description}".strip(),
                    (facet_description, value_description),
                )
            )
        if query:
            if descriptions.get("brand"):
                description = description.replace(
                    "and", "about", 1
                )  # So that its "Answer robotoff questions about the <brand_name> ..."
                # and not "Answer robotoff questions and the <brand_name> ..."
                # when two facets are given (including brand)
            urls.add((f"{questions_url}?{urlencode(query)}", description, (None, None)))

        t_description = "Answer questions from Robotoff"
        for id, val in enumerate(sorted(urls)):
            url, des, (facet_name, facet_value) = val
            final_description = _(f"{t_description} {des}").format(
                brand_name=description_values.get("brand_name"),
                country=description_values.get("country"),
                facet_name=facet_name,
                facet_value=facet_value,
            )
            html.append(
                {
                    "element_type": "text",
                    "text_element": {
                        "html": f"<ul><li><p><a href='{url}' class='button small'><em>{final_description}</em>"
                        + "</a></p></li></ul>"
                    },
                },
            )

         # for logos
        logos_url = settings().HUNGER_GAME + "/logos"
        description_msgids = [
            {
                "description": "Annotate the {facet_value} {facet_name} more",
                "url": f"{logos_url}/deep-search?type={{facet_name}}&value_tag={{facet_value}}",
            },
            {
                "description": "Kickstart annotation for the {facet_value} {facet_name}",
                "url": (
                    f"{logos_url}/product-search?value_tag={{facet_value}}"
                    f"&tagtype={{facet_name}}"
                ),
            },
        ]

        for k, v in facets_logo.items():
            for i in description_msgids:
                des = format_translation(
                    _(i["description"]), values={"facet_value": v, "facet_name": k}
                )

                url = i["url"].format(facet_name=k, facet_value=v)

                if k == "label":
                    url = url.replace("tagtype", "type")

                html.append(
                    {
                        "element_type": "text",
                        "text_element": {
                            "html": f"<ul><li><p><a href='{url}' class='button small'><em>{des}</em>"
                            + "</a></p></li></ul>"
                        },
                    },
                )

        kp = {"HungerGames": {"elements": html, "title_element": {"title": "Hunger Games (Contribute by playing)"}}}

        return kp if urls else None

    @no_exception()
    async def data_quality_kp(self) -> dict:
        """
        Get data corresponding to differnet facet
        """
        path = ""
        description = ""
        if self.facet == "country":
            self.country = self.value
            country_code = country_name_to_alpha2(value=self.value)
            url = openFoodFacts(country_code)
            path = ""
            self.facet = self.value = None
        if self.sec_facet == "country":
            self.country = self.sec_value
            country_code = country_name_to_alpha2(value=self.sec_value)
            url = openFoodFacts(country_code)
            path = ""
            self.sec_facet = self.sec_value = None
        if self.country is not None:
            country_code = country_name_to_alpha2(value=self.country)
            url = openFoodFacts(country_code)
            path = ""
            description += f"{self.country} "
        if self.country is None:
            url = openFoodFacts()
        if self.value is None:
            path = "facets"
        if self.value is not None:
            path += f"facets/{pluralize(self.facet)}/{self.value}"
            description += f"{self.facet} {self.value}"
        # Checking if secondary facet is provided
        if self.sec_facet is not None:
            path += f"/{pluralize(self.sec_facet)}"
            description += f" {self.sec_facet}"
        if self.sec_value is not None:
            path += f"/{self.sec_value}"
            description += f" {self.sec_value}"
        data = await data_quality(url=url, path=path)

        return {
            "Quality": {
                "elements": [
                    {
                        "element_type": "text",
                        "text_element": {
                            "html": data.text,
                            "source_text": data.title,
                            "source_url": f"{data.source_url}/data-quality-errors",
                        },
                    }
                ],
                "title_element": {"title": f"{data.description} {description}"},
            },
        }

    @no_exception()
    async def last_edits_kp(self) -> dict:
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
            country_code = country_name_to_alpha2(value=self.value)
            url = openFoodFacts(country_code)
            self.facet = self.value = None
        if self.sec_facet == "country":
            self.country = self.sec_value
            country_code = country_name_to_alpha2(value=self.sec_value)
            url = openFoodFacts(country_code)
            self.sec_facet = self.sec_value = None
        if self.country is not None:
            country_code = country_name_to_alpha2(value=self.country)
            url = openFoodFacts(country_code)
            source_url = f"{url}?sort_by=last_modified_t"
            description += f"{self.country} "
        if self.country is None:
            url = openFoodFacts()
        if self.facet is not None:
            description += f"{self.facet}"
            source_url = f"{url}/{self.facet}?sort_by=last_modified_t"
        if self.value is not None:
            query[f"{pluralize(facet=self.facet)}_tags_en"] = self.value
            description += f" {self.value}"
            source_url = f"{url}/{self.facet}/{self.value}?sort_by=last_modified_t"
        if self.sec_value and self.sec_facet is not None:
            query[f"{pluralize(facet=self.sec_facet)}_tags_en"] = self.sec_value
            description += f" {self.sec_facet} {self.sec_value}"
            source_url = f"{url}/{self.facet}/{self.value}/{self.sec_facet}/{self.sec_value}?sort_by=last_modified_t"  # noqa: E501
        data = await last_edit(url=url, query=query)
        return {
            "LastEdits": {
                "elements": [
                    {
                        "element_type": "text",
                        "text_element": {
                            "html": data.text,
                            "source_text": data.title,
                            "source_url": source_url,
                        },
                    },
                ],
                "title_element": {"title": f"{data.description} {description}"},
            },
        }

    @no_exception()
    async def _wikidata_kp(self, facet, value) -> Optional[dict]:
        query = {}
        if value:
            query["tagtype"] = pluralize(facet=facet)
            query["fields"] = "wikidata"
            query["tags"] = value
            return await wikidata_helper(query=query, value=value)

    async def wikidata_kp(self) -> Optional[dict]:
        """
        Return knowledge panel for wikidata
        """
        entities = set()
        params = ((self.facet, self.value), (self.sec_facet, self.sec_value))
        for facet, value in params:
            if facet not in Taxonomies.list():
                continue
            entity = await self._wikidata_kp(facet=facet, value=value)
            if entity is not None:
                entities.add(entity)

        html = []
        info = []
        for id, val in enumerate(entities):
            html.append(
                {
                    "element_type": "text",
                    "text_element": {
                        "html": f"<ul><p><em>{val.label_tag}</em></p><p>{val.description_tag}</p>",  # noqa: E501
                        "source_text": "wikidata",
                        "source_url": settings().WIKIDATA + val.entity_id,
                    },
                }
            )
            if val.image_url != "":
                info.append(f"""<p><img alt='wikidata image' src='{val.image_url}'></p>""")
            if val.wikipedia_relation != "":
                info.append(f"""<li><a href='{val.wikipedia_relation}'>Wikipedia</a></li>""")
            if val.OSM_relation != "":
                info.append(f"""<li><a href='{val.OSM_relation}'>OpenStreetMap relation</a></li>""")
            if val.INAO_relation != "":
                info.append(f"""<li><a href='{val.INAO_relation}'>French INAO relation</a></li>""")
            info.append("</ul>")
            link = "".join(info)
            html.append(
                {
                    "element_type": "text",
                    "text_element": {"html": link},
                }
            )
            info.clear()
        panel = {"WikiData": {"elements": html, "title_element": {"title": "wikidata"}}}
        return panel if entities else None
