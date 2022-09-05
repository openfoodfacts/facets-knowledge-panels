# Project Setup
You may choose Docker-compose(recommended), or Through virtual env 

### Through Docker

- Prerequisite - [Docker](https://docs.docker.com/get-docker/)

After forking the repository

to build:
```bash
docker-compose build
```

to run:
```bash
docker-compose up
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
```
uvicorn app.main:app --reload
```
- Checkout your local host `http://127.0.0.1:8000/` with the endpoints or /docs for documentation