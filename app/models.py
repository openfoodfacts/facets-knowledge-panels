from pydantic import BaseModel
from enum import Enum

class Facetname(str, Enum):
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
    

