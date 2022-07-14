from enum import Enum

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
        return [c.value for c in  FacetName]


class HungerGameFilter(str, Enum):
    label = "label"
    category = "category"
    brand = "brand"
    product_weight = "product_weight"

    @staticmethod
    def list():
        return [c.value for c in HungerGameFilter]
