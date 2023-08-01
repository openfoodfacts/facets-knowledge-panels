from enum import Enum
from typing import Optional, TypedDict

import inflect
import pycountry
from fastapi import Query
from pydantic import BaseModel, Field


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


def alpha2_to_country_name(value: Optional[str]):
    """
    Helper function to return country name for aplha2 code
    """
    if value is not None and len(value) == 2:
        country = pycountry.countries.get(alpha_2=value)
        if country is not None:
            return f"{country.name}"
    return value


def country_name_to_alpha2(value: Optional[str]):
    """
    Helper function that return alpha2 code for country name
    """
    country = pycountry.countries.get(name=value)
    if country is not None:
        return f"{(country.alpha_2).lower()}-en"
    return "world"


inflectEngine = inflect.engine()


def pluralize(facet: str):
    """
    Return plural form of facet
    """
    return facet if facet == "packaging" else inflectEngine.plural_noun(facet)


def singularize(facet: Optional[str]):
    """
    Return singular form of facet
    """
    if facet is not None:
        return (
            facet if not inflectEngine.singular_noun(facet) else inflectEngine.singular_noun(facet)
        )


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
            description="To return knowledge panels in native language, default lang: `en`.",
        )
        return query

    def country_query():
        query = Query(
            default=None,
            title="Country tag string",
            description="To return knowledge panels for specific country, ex: `france` or `fr`.",
        )
        return query


# --------------------------------------------
# Response model class for the knowledge panels
# --------------------------------------------


class BaseTitleElement(BaseModel):
    """An element containing a title"""

    title: str = Field(
        description="title of the panel",
    )


class BaseTextElement(BaseModel):
    """An element with simple HTML to display"""

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
    """Element container"""

    element_type: str = Field(
        description="The type of the included element object."
        "The type also indicates which field contains the included element object. "
        """e.g. if the type is "text", the included element object will be in the "text_element" field.""",  # noqa: E501
    )
    text_element: BaseTextElement = Field(
        description="A text in simple HTML format to display.",
    )


class KnowledgePanelItem(BaseModel):
    """A Panel, made of multiple sub elements"""

    elements: Optional[list[BaseElement]] = None
    title_element: BaseTitleElement


class HungerGamePanel(TypedDict, total=False):
    """Panel linking to Hunger Games"""

    HungerGames: KnowledgePanelItem


class DataQualityPanel(TypedDict, total=False):
    """Panel with elements of data quality"""

    Quality: KnowledgePanelItem


class LastEditsPanel(TypedDict, total=False):
    """Panel reporting last edits for the facet"""

    LastEdits: KnowledgePanelItem


class WikidataPanel(TypedDict, total=False):
    """Panel with informations taken from wikidata"""

    WikiData: KnowledgePanelItem


class KnowledgePanel(HungerGamePanel, DataQualityPanel, LastEditsPanel, WikidataPanel):
    pass


class FacetResponse(BaseModel):
    # Return facetresponse l.e, all differnt knowledge panel
    knowledge_panels: Optional[KnowledgePanel] = None
