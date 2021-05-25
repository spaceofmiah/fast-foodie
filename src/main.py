import logging
from typing import Optional, List
from fastapi import FastAPI


app = FastAPI()
logger = logging.getLogger(__name__)

food_db: List[str] = ["German Potatoes Slice", "Gernished Peppered Snake"]


@app.get("/foods")
def foods():
    return {"results": food_db}


@app.get("/foods/{id}")
def food(id: int):
    try:
        return food_db[id]
    except IndexError:
        return {"detail": "Not Found"}
