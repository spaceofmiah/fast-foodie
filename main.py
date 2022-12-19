import logging
from typing import List, Dict, Union

from sqlalchemy.orm import Session

from fastapi import (
    HTTPException, 
    FastAPI, 
    Depends, 
    status, 
    Query, 
    Path
)

from db.services import foods as food_service, users as user_service
from db.schemas import foods as food_schema, users as user_schema
from db.initializer import get_db
from utils.password_utils import hash_password



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
def list_foods(
    session:Session=Depends(get_db), 
    q:Union[str, None]=Query(
        default=None,
        title="query",
        description="search & returns food list by name containing query"
    )
):
    """Retrieve all food records"""
    return food_service.db_list(session=session, query=q)

@app.post(
    '/foods/', 
    tags=['foods'],
    response_model=food_schema.Food
)
def create_food(food:food_schema.FoodCreate, session:Session=Depends(get_db)):
    """Create a food instance"""
    return food_service.db_create(session=session, food=food)

@app.get(
    '/foods/{food_id}', 
    tags=['foods'],
    response_model=food_schema.Food
)
def get_food(
    *,
    session:Session=Depends(get_db),
    food_id:int=Path(default=None, description="ID of the food to retrieve", gt=0), 
):
    """Retrieve a unique food instance"""
    try:
        return food_service.db_get(session=session, food_id=food_id)
    except:
        logger.exception("something went wrong")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not Found"
        ) 

@app.delete(
    '/foods/{food_id}/', 
    tags=['foods'],
    response_model=Dict
)
def delete_food(
    *,
    session:Session=Depends(get_db),
    food_id:int=Path(default=None, description="ID of the food to delete", gt=0),  
):
    """Deletes a unique food instance"""
    try:
        food_service.db_delete(session=session, food_id=food_id)
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not Found"
        ) 

    return {"detail": "Request handled successfully"}


@app.put(
    "/foods/{food_id}/", 
    tags=['foods'],
    response_model=food_schema.Food
)
def update_food(
    *,
    food:food_schema.FoodUpdate, 
    session:Session=Depends(get_db),
    food_id:int=Path(default=None, description="ID of the food to update", gt=0), 
):
    """Update an existing food instance"""
    try:
        db_food:food_model.Food = food_service.db_get(session=session, food_id=food_id)
    except:
        logger.exception("Error while retrieving food instance")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")

    food_service.db_update(session=session, food_id=food_id, food=food)
    return db_food

@app.get('/users', tags=['users'], response_model=List[user_schema.User])
def list_users(session:Session=Depends(get_db)):
    """Retrieves all available users"""
    return user_service.db_list(session)


@app.post('/users', tags=['users'], response_model=user_schema.User)
def create_user(
    *,
    session:Session=Depends(get_db), 
    user:user_schema.UserCreate
):
    """Create a new user

        **first_name** : first name of the user to be created

        **last_name**  : last name of the user to be created

        **email** * : unique email address of user

        **password**   : user's password
    """
    user.hashed_password = hash_password(user.hashed_password)
    return user_service.db_create(session=session, user=user)