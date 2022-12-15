from typing import List
import logging

from fastapi import FastAPI
from db.services import food_services


app = FastAPI()
logger = logging.getLogger(__name__)

food_db: List[str] = ["German Potatoes Slice", "Gernished Peppered Snake"]


@app.get("/foods")
def foods():
    """
    Handles request to retrieve all meals in the database
    """
    return food_services.DQL.retrieve_foods()


@app.get("/foods/{id}")
def food(id: int):
    try:
        return food_db[id]
    except IndexError:
        return {"detail": "Not Found"}
