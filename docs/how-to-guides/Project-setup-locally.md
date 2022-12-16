# Project Setup
You may choose Docker-compose(recommended), or Through virtual env 

### Through Docker[Recommended]

- Prerequisite - [Docker](https://docs.docker.com/get-docker/)

After forking the repository

to build:
```bash
docker-compose build
```
or
```bash
make docker_build
```

to run:
```bash
docker-compose up
```
or
```bash
make docker_up
```

- Visit `http://127.0.0.1/` with the endpoints or /docs for documentation

### Through virtual env

- Prerequisite - [Python](https://www.python.org/downloads/)
- After forking the repository
- Create [virtual env](https://docs.python.org/3/library/venv.html)
- Install requirements.txt
```
pip install -r requirements.txt
```

- For setup the environment, please copy "external urls" value from ".env" file to "Settings" class of "config.py".
- After this step your local "Settings" class in "config.py" look like this:

```
class Settings(BaseSettings):

    HUNGER_GAME: str = "https://hunger.openfoodfacts.org/questions"
    OPENFOODFACTS: str = "openfoodfacts.org"
    WIKIDATA: str = "https://www.wikidata.org/wiki/"
    TAXONOMY: str = "https://world.openfoodfacts.org/api/v2/taxonomy"
    INAO: str = "https://www.inao.gouv.fr/produit/"
    OPENSTREETMAP: str = "https://www.openstreetmap.org/relation/"

    class Config:
        env_prefix = "FACETS_"
```

- Now you ready to runserver.
```
uvicorn app.main:app --reload
```
- Checkout your local host `http://127.0.0.1:8000/` with the endpoints or /docs for documentation