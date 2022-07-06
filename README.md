# facets-knowledge-panels
Providing knowledge panels for a particular open food fact facet (category, brand, etc...)

## why facets-knowledge-panels?

- Apps don't have to add special code for each panel (e.g. looking at the array of ingredients and additives, the values of nutrients etc.)
- Apps don't need to load and update taxonomies to interpret the returned data
- Translations are managed by the server, and we can use Crowdin to crowdsource them in many languages
- If desired, apps can decide to use new product attributes added on the server without requiring app changes

## Project Setup

### Through Docker

- After forking the repository
```
docker-compose up
```
- Visit `http://127.0.0.1/` with the endpoints

### Through virtual env

- After forking the repository
- Create [virtual env](https://docs.python.org/3/library/venv.html)
- Install requirements.txt
```
pip install -r requirements.txt
```
```
cd app
```
```
uvicorn main:app --reload
```
- Checkout your local host `http://127.0.0.1:8000/` with the endpoints

## Testing

- Checkout `tests` directory
```
pytest 
```

