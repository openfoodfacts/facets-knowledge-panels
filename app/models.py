from enum import Enum
import inflect

"""Library to correctly generate plurals, singular nouns, ordinals, indefinite articles convert numbers to words. 
https://pypi.org/project/inflect/ """

import pycountry
from pydantic import BaseModel


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


def country_to_ISO_code(value: str):
    country_data = pycountry.countries.get(name=value)
    country_iso_code = country_data.alpha_2
    return country_iso_code.lower()
