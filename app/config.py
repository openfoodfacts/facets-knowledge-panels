from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    HUNGER_GAME: str
    OPENFOODFACTS: str
    WIKIDATA: str
    TAXONOMY: str
    INAO: str
    OPENSTREETMAP: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def settings():
    return Settings()


def openFoodFacts(country):
    return str("https://" + country + "." + settings().OPENFOODFACTS)
