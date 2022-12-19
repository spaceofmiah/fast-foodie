from typing import Union, List, Dict
import logging

from fastapi import (
	HTTPException, 
	APIRouter, 
	Depends, 
	status,
	Query, 
	Path, 
)
from sqlalchemy.orm import Session

from db.initializer import get_db
from db.models import foods as model
from db.schemas import foods as schema
from db.services import foods as db_service

from utils import auth


router = APIRouter()
logger = logging.getLogger(__name__)



@router.get(
    "/foods", 
    tags=['foods'],
    response_model=List[schema.Food],
)
def list(
    session:Session=Depends(get_db), 
    q:Union[str, None]=Query(
        default=None,
        title="query",
        description="search & returns food list by name containing query"
    )
):
    """Retrieve all food records"""
    return db_service.db_list(session=session, query=q)

@router.post(
    '/foods/', 
    tags=['foods'],
    response_model=schema.Food,
)
def create(
    food:schema.FoodCreate, 
    session:Session=Depends(get_db),
    token:str = Depends(auth.oauth2_scheme), 
):
    """Create a food instance"""
    return db_service.db_create(session=session, food=food)

@router.get(
    '/foods/{food_id}', 
    tags=['foods'],
    response_model=schema.Food
)
def get(
    *,
    session:Session=Depends(get_db),
    food_id:int=Path(default=None, description="ID of the food to retrieve", gt=0), 
):
    """Retrieve a unique food instance"""
    try:
        return db_service.db_get(session=session, food_id=food_id)
    except:
        logger.exception("something went wrong")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not Found"
        ) 

@router.delete(
    '/foods/{food_id}/', 
    tags=['foods'],
    response_model=Dict,
)
def delete(
    *,
    token:str = Depends(auth.oauth2_scheme),
    session:Session=Depends(get_db),
    food_id:int=Path(default=None, description="ID of the food to delete", gt=0),  
):
    """Deletes a unique food instance"""
    try:
        db_service.db_delete(session=session, food_id=food_id)
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not Found"
        )
    return {"detail": "Request handled successfully"}

@router.put(
    "/foods/{food_id}/", 
    tags=['foods'],
    response_model=schema.Food,
)
def update(
    *,
    token:str = Depends(auth.oauth2_scheme),
    food:schema.FoodUpdate, 
    session:Session=Depends(get_db),
    food_id:int=Path(default=None, description="ID of the food to update", gt=0), 
):
    """Update an existing food instance"""
    try:
        db_food:model.Food = db_service.db_get(session=session, food_id=food_id)
    except:
        logger.exception("Error while retrieving food instance")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")

    db_service.db_update(session=session, food_id=food_id, food=food)
    return db_food
