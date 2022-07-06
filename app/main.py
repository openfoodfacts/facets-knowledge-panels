from typing import Union

from fastapi import FastAPI

app = FastAPI()


@app.get("/brand/president")
def read_root():
    return {"knowledge_panels": []}


