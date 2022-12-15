import logging
from typing import List

from sqlalchemy.orm import Session

from fastapi import FastAPI, Depends

from db.services import foods as food_service
from db.schemas import foods as food_schema
from db.initializer import get_db



app = FastAPI()
logger = logging.getLogger(__name__)


@app.get("/foods", response_model=List[food_schema.Food])
def list_foods(session:Session=Depends(get_db)):
    """Retrieve all food records"""
    return food_service.list(session=session)

@app.post('/create-food/', response_model=food_schema.Food)
def create_food(food:food_schema.FoodCreate, session:Session=Depends(get_db)):
    """Create a food instance"""
    return food_service.create(session=session, food=food)

