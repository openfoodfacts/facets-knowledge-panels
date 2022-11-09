from enum import Enum
from typing import Optional, Union

import inflect
import pycountry
from fastapi import Query
from pydantic import BaseModel, Field


class FacetName(str, Enum):
    country = "country"
    nutrition_grade = "nutrition_grade"
    nova_group = "nova_group"
    brand = "brand"
    category = "category"
    label = "label"
    packaging = "packaging"
    origin_of_ingredient = "origin"
    manufacturing_place = "manufacturing_place"
    packager_code = "packager_code"
    ingredient = "ingredient"
    additive = "additive"
    vitamin = "vitamin"
    mineral = "mineral"
    amino_acid = "amino_acid"
    nucleotide = "nucleotide"
    allergen = "allergen"
    trace = "trace"
    language = "language"
    contributor = "contributor"
    state = "state"
    data_source = "data_source"
    entry_date = "entry_date"
    last_edit_date = "last_edit_date"
    last_check_date = "last_check_date"
    other_nutritional_substances = "other_nutritional_substances"
    team = "team"

    @staticmethod
    def list():
        return [c.value for c in FacetName]


class HungerGameFilter(str, Enum):
    label = "label"
    category = "category"
    country = "country"
    brand = "brand"
    product_weight = "product_weight"

    @staticmethod
    def list():
        return [c.value for c in HungerGameFilter]


class Taxonomies(str, Enum):
    country = "country"
    nova_group = "nova_group"
    brand = "brand"
    category = "category"
    label = "label"
    packaging = "packaging"
    ingredient = "ingredient"
    additive = "additive"
    vitamin = "vitamin"
    mineral = "mineral"
    amino_acid = "amino_acid"
    nucleotide = "nucleotide"
    allergen = "allergen"
    state = "state"
    origin_of_ingredient = "origin"
    language = "language"
    other_nutritional_substances = "other_nutritional_substances"

    @staticmethod
    def list():
        return [c.value for c in Taxonomies]


def country_to_ISO_code(value: str):
    """
    Helper function that return ISO code for country
    """
    country_data = pycountry.countries.get(name=value)
    if country_data is not None:
        country_iso_code = country_data.alpha_2
        return f"{country_iso_code.lower()}-en"
    return "world"


def facet_plural(facet: str):
    """
    Return plural of facet
    """
    p = inflect.engine()
    plural = p.plural(facet)
    facet_plural = plural
    if facet == "packaging":
        facet_plural = facet

    return facet_plural


class QueryData:
    """
    Helper class for handling repetition of query
    """

    def facet_tag_query():

        query = Query(
            title="Facet tag string",
            description="Facet tag string for the items to search in the database eg:- `category` etc.",  # noqa: E501
        )
        return query

    def value_tag_query():
        query = Query(
            default=None,
            title="Value tag string",
            description="value tag string for the items to search in the database eg:-`en:beers` etc.",  # noqa: E501
        )
        return query

    def secondary_facet_tag_query():
        query = Query(
            default=None,
            title="secondary facet tag string",
            description="secondary facet tag string for the items to search in the database eg:-`brand` etc.",  # noqa: E501
        )
        return query

    def secondary_value_tag_query():
        query = Query(
            default=None,
            title="secondary value tag string",
            description="secondary value tag string for the items to search in the database eg:-`lidl` etc.",  # noqa: E501
        )
        return query

    def language_code_query():
        query = Query(
            default=None,
            title="language code string",
            description="To return knowledge panels in native language, defualt lang: `en`.",
        )
        return query

    def country_query():
        query = Query(
            default=None,
            title="Country tag string",
            description="To return knowledge panels for specific country, ex: `france`.",
        )
        return query


# --------------------------------------------
# Response model class for the knowledge panels
# --------------------------------------------


class BaseTitleElement(BaseModel):
    # Containing title element
    title: str = Field(
        description="title of the panel",
    )


class BaseTextElement(BaseModel):
    # Conataning text element
    html: Optional[str] = Field(
        default=None,
        description="Text to display in HTML format",
    )
    source_text: Optional[str] = Field(
        description="name of the source",
    )

    source_url: Optional[str] = Field(
        description="Link to the source",
    )


class BaseElement(BaseModel):
    # Contains base elements of panel

    element_type: str = Field(
        description="The type of the included element object."
        "The type also indicates which field contains the included element object. "
        """e.g. if the type is "text", the included element object will be in the "text_element" field.""",  # noqa: E501
    )
    text_element: BaseTextElement = Field(
        description="A text in simple HTML format to display.",
    )


class KnowledgePanelItem(BaseModel):
    # Helper class for reccuring item
    elements: Optional[list[BaseElement]] = None
    title_element: BaseTitleElement


class HungerGamePanel(BaseModel):
    # return hungergamespanel response
    hunger_game: KnowledgePanelItem


class DataQualityPanel(BaseModel):
    # return dataqualitypanel response
    Quality: KnowledgePanelItem


class LastEditsPanel(BaseModel):
    # return lasteditspanel response
    LastEdits: KnowledgePanelItem


class WikidataPanel(BaseModel):
    # return wikidatapanel response
    WikiData: KnowledgePanelItem


KnowledgePanel = Union[HungerGamePanel, DataQualityPanel, LastEditsPanel, WikidataPanel]


class FacetResponse(BaseModel):
    # Return facetresponse l.e, all differnt knowledge panel
    knowledge_panels: Optional[list[KnowledgePanel]] = None
