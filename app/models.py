from enum import Enum
from typing import Optional, Union

import inflect
import pycountry
from pydantic import BaseModel


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


class ElementsForDataQualityAndLastEdits(BaseModel):
    element_type: str
    text_element: Optional[str] = None


class ElementsForHungerGame(BaseModel):
    id: int
    element_type: str
    text_element: str


class ItemsForDataQualityAndLastEdits(BaseModel):
    title: str
    subtitle: Optional[str] = None
    source_url: Optional[str] = None
    elements: Optional[list[ElementsForDataQualityAndLastEdits]] = None


class TextItemWikiData(BaseModel):
    element_type: str
    text_element: str


class LinksItemWikiData(BaseModel):
    element_type: str
    wikipedia: Optional[str] = None
    image_url: Optional[str] = None
    open_street_map: Optional[str] = None
    INAO: Optional[str] = None


WikidataPanel = Union[TextItemWikiData, LinksItemWikiData]


class ElementsWikidata(BaseModel):
    id: int
    subtitle: Optional[str] = None
    source_url: Optional[str] = None
    elements: Optional[list[WikidataPanel]] = None


class WikidataKnowledgePanelItem(BaseModel):
    title: str
    elements: Optional[list[ElementsWikidata]] = None


class HungerGameKnowledgePanelItem(BaseModel):
    title: str
    elements: Optional[list[ElementsForHungerGame]] = None


class HungerGameResponse(BaseModel):
    hunger_game: HungerGameKnowledgePanelItem


class DataQualityResponse(BaseModel):
    Quality: ItemsForDataQualityAndLastEdits


class LastEditsResponse(BaseModel):
    LastEdits: ItemsForDataQualityAndLastEdits


class WikidataResponse(BaseModel):
    WikiData: WikidataKnowledgePanelItem


KnowledgePanels = Union[
    HungerGameResponse, DataQualityResponse, LastEditsResponse, WikidataResponse
]


class FacetResponse(BaseModel):
    knowledge_panels: Optional[list[KnowledgePanels]] = None
