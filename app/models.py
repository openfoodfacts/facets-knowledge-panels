from enum import Enum
import pycountry
import inflect


class FacetName(str, Enum):
    country = "country"
    nutrition_grade = "nutrition-grade"
    nova_group = "nova-group"
    brand = "brand"
    category = "category"
    label = "label"
    packaging = "packaging"
    origin_of_ingredient = "origin"
    manufacturing_place = "manufacturing-place"
    packager_code = "packager-code"
    ingredient = "ingredient"
    additive = "additive"
    vitamin = "vitamin"
    mineral = "mineral"
    amino_acid = "amino-acid"
    nucleotide = "nucleotide"
    allergen = "allergen"
    trace = "trace"

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
