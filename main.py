import logging
from typing import List, Dict, Union

from sqlalchemy.orm import Session

from fastapi import FastAPI, Depends, HTTPException, status

from db.services import foods as food_service
from db.schemas import foods as food_schema
from db.initializer import get_db



app = FastAPI(
    title="FastFoodie",
    contact={
        "name": "spaceofmiah",
        "email": "spaceofmiah@gmail.com",
        "url": "https://spaceofmiah.github.io",
    },
    description="Learning fastapi using a demo food api standard",
    terms_of_service="https://github.com/spaceofmiah/fast-foodie",
)
logger = logging.getLogger(__name__)


@app.get(
    "/foods", 
    tags=['foods'],
    response_model=List[food_schema.Food],
)
def list_foods(session:Session=Depends(get_db)):
    """Retrieve all food records"""
    return food_service.list(session=session)

@app.post(
    '/create-food/', 
    tags=['foods'],
    response_model=food_schema.Food
)
def create_food(food:food_schema.FoodCreate, session:Session=Depends(get_db)):
    """Create a food instance"""
    return food_service.create(session=session, food=food)

@app.get(
    '/foods/{food_id}/', 
    tags=['foods'],
    response_model=Union[food_schema.Food, Dict[str, str]]
)
def get_food(food_id:int, session:Session=Depends(get_db)):
    """Retrieve a unique food instance"""
    try:
        return food_service.get(session=session, food_id=food_id)
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not Found"
        ) 

@app.delete(
    '/foods/{food_id}/', 
    tags=['foods'],
    response_model=Dict[str, str]
)
def delete_food(food_id:int, session:Session=Depends(get_db)):
    """Deletes a unique food instance"""
    try:
        food_service.delete(session=session, food_id=food_id)
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not Found"
        ) 

    return {"msg": "Request handled successfully"}

