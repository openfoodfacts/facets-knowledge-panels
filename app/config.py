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


settings = Settings()


def openFoodFacts(country):
    return str("https://" + country + "." + settings.OPENFOODFACTS)
