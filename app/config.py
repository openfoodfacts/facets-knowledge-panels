from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    """
    default values are here for making  project setup(Through virtaul env) easy for contributors.
    """

    HUNGER_GAME: str = "https://hunger.openfoodfacts.org/questions"
    OPENFOODFACTS: str = "openfoodfacts.org"
    WIKIDATA: str = "https://www.wikidata.org/wiki/"
    TAXONOMY: str = "https://world.openfoodfacts.org/api/v2/taxonomy"
    INAO: str = "https://www.inao.gouv.fr/produit/"
    OPENSTREETMAP: str = "https://www.openstreetmap.org/relation/"

    class Config:
        env_prefix = "FACETS_"


@lru_cache()
def settings():
    return Settings()


def openFoodFacts(country):
    return str("https://" + country + "." + settings().OPENFOODFACTS)
