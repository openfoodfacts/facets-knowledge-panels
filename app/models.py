from enum import Enum
from typing import Union
from pydantic import BaseModel
import inflect
import pycountry


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
    country_iso_code = country_data.alpha_2
    return country_iso_code.lower()


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


class ElementsItem(BaseModel):
    element_type: str
    text_element: Union[str, None] = None


class KnowledgePanelItem(BaseModel):
    title: str
    subtitle: Union[str, None] = None
    source_url: Union[str, None] = None
    elements: Union[list[ElementsItem], None] = None


class WikidataElementsItem(BaseModel):
    element_type: str
    image_url: Union[str, None] = None
    wikipedia: Union[str, None] = None
    open_street_map: Union[str, None] = None
    INAO: Union[str, None] = None


WikidataPanel = Union[ElementsItem, WikidataElementsItem]


class WikidataKnowledgePanelItem(BaseModel):
    title: str
    subtitle: Union[str, None] = None
    source_url: Union[str, None] = None
    elements: Union[list[WikidataPanel], None] = None


class HungerGameKnowledgePanelItem(BaseModel):
    title: str
    subtitle: Union[str, None] = None
    elements: Union[list[ElementsItem], None] = None


class HungerGameResponse(BaseModel):
    hunger_game: HungerGameKnowledgePanelItem


class DataQualityResponse(BaseModel):
    Quality: KnowledgePanelItem


class LastEditsResponse(BaseModel):
    LastEdits: KnowledgePanelItem


class WikidataResponse(BaseModel):
    WikiData: WikidataKnowledgePanelItem


KnowledgePanel = Union[HungerGameResponse, DataQualityResponse, LastEditsResponse, WikidataResponse]


class FacetResponse(BaseModel):
    knowledge_panels: Union[list[KnowledgePanel], None] = None
