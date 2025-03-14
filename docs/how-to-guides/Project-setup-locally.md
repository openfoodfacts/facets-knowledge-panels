# Project Setup
You may choose Docker compose(recommended), or Through virtual env 

### Through Docker[Recommended]

- Prerequisite - [Docker](https://docs.docker.com/get-docker/)

After forking the repository

to build:
```bash
docker compose build
```
or
```bash
make build
```

to run:
```bash
docker compose up
```
or
```bash
make up
```

- Visit `http://127.0.0.1/` with the endpoints or /docs for documentation

### Through virtual env

- Prerequisite 
  - [Python](https://www.python.org/downloads/)
  - use a [git bash](https://gitforwindows.org/#bash) console to run the commands below
- After forking the repository
- Create [virtual env](https://docs.python.org/3/library/venv.html)
- Activate you virtual environment `. path/to/virtualenv/bin/activate`
- Install requirements.txt
```
pip install -r requirements.txt
```


- Load the environment variables: `. load_env.sh`
- Now you ready to runserver.
```
uvicorn app.main:app --reload
```
- Checkout your local host `http://127.0.0.1:8000/` with the endpoints or /docs for documentation
