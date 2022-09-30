from enum import Enum
from typing import Optional, Union

import inflect
import pycountry
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


# --------------------------------------------
# Response model class for the knowledge panels
# --------------------------------------------


class TextFacet(BaseModel):
    """Base facet containing text"""

    element_type: str
    text_element: Optional[str] = Field(
        default=None,
        description="Html value with desciption of the item",
    )


class HungerGameElement(TextFacet):
    id: int


class DataQualityAndLastEditsItem(BaseModel):
    """
    contains link and text elements
    """

    title: str
    subtitle: Optional[str] = Field(
        default=None,
        description="Short description of different facet and value in which it computes the data. ",  # noqa: E501
    )
    source_url: Optional[str] = Field(
        default=None,
        description="Link to the source of the data l.e, OpenFoodFacts page.",
    )
    elements: Optional[list[TextFacet]] = None


class TextFacetWikiData(TextFacet):
    """Base facet for wikidata conating text elements"""

    text_element: str = Field(
        description="label for given facet coming from wikidata.",
    )


class WikiDataLinksItem(BaseModel):
    """
    Contains all different links fom wikidata
    """

    element_type: str
    wikipedia: Optional[str] = Field(
        default=None,
        description="Link to the wikipedia for the given parameter.",
    )
    image_url: Optional[str] = Field(
        default=None,
        description="Link for the wikidata image.",
    )
    open_street_map: Optional[str] = Field(
        default=None,
        description="link to the OpenStreetMap relation through wikidata.",
    )
    INAO: Optional[str] = Field(
        default=None,
        description="link to the INAO(Institut national de l'origine et de la qualité) for the given parameter.",  # noqa: E501
    )


WikidataPanel = Union[TextFacetWikiData, WikiDataLinksItem]


class WikidtaElement(BaseModel):
    """
    contains wikidata description and text elements
    """

    id: int
    subtitle: Optional[str] = Field(
        default=None,
        description="description of the item coming from wikidata.",
    )
    source_url: Optional[str] = Field(
        default=None,
        description="Link to the source of the data l.e, wikidata page.",
    )
    elements: Optional[list[WikidataPanel]] = None


class BasePanel(BaseModel):
    title: str
    elements: list


class WikidataKnowledgePanelItem(BasePanel):
    elements: Optional[list[WikidtaElement]] = None


class HungerGameKnowledgePanelItem(BasePanel):
    elements: Optional[list[HungerGameElement]] = None


class HungerGamePanel(BaseModel):
    # return hungergamespanel response
    hunger_game: HungerGameKnowledgePanelItem


class DataQualityPanel(BaseModel):
    # return dataqualitypanel response
    Quality: DataQualityAndLastEditsItem


class LastEditsPanel(BaseModel):
    # return lasteditspanel response
    LastEdits: DataQualityAndLastEditsItem


class WikidataPanel(BaseModel):
    # return wikidatapanel response
    WikiData: WikidataKnowledgePanelItem


KnowledgePanel = Union[HungerGamePanel, DataQualityPanel, LastEditsPanel, WikidataPanel]


class FacetResponse(BaseModel):
    # Return facetresponse l.e, all differnt knowledge panel
    knowledge_panels: Optional[list[KnowledgePanel]] = None
