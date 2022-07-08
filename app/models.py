from pydantic import BaseModel
from enum import Enum

class Facetname(str, Enum):
    countries = "countries"
    nutrition_grades = "nutrition-grades"
    nova_groups = "nova-groups"
    brands = "brands"
    categories = "categories"
    labels = "labels"
    packaging = "packaging"
    origins_of_ingredients = "origins"
    manufacturing_places = "manufacturing-places"
    packager_codes = "packager-codes"
    ingredients = "ingredients"
    additives = "additives"
    vitamins = "vitamins"
    minerals = "minerals"
    amino_acids = "amino-acids"
    nucleotides = "nucleotides"
    allergens = "allergens"
    traces = "traces"
    
class Facetvalue(BaseModel):
    facet_value: str()
