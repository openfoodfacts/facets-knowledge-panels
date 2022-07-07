# facets-knowledge-panels
Providing knowledge panels for a particular open food fact facet (category, brand, etc...)

## why facets-knowledge-panels?

Provides applications with a set of informative or actionable items which are contextual to a specific facet.

The primary goal is to allow high level contributions by users that maybe interested in a particular subset of the database, like a particular food category or a brand, a location, etc...

We reuse the knowledge panel format, which remove the need for the application to change as the server side code change, or to implement specific business logic.


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

