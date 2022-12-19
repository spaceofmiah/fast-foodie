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
from fastapi.security import OAuth2PasswordRequestForm

from db.services import foods as food_service, users as user_service
from db.schemas import foods as food_schema, users as user_schema
from settings.dev import TOKEN_URL_PATH
from db.initializer import get_db
from utils import auth



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


@app.post(f"/{TOKEN_URL_PATH}", response_model=Dict[str, str])
def login(
    auth_form:OAuth2PasswordRequestForm=Depends(), 
    session:Session=Depends(get_db),
):
    """Processes user's authentication request

        **username** * : Unique identifier e.g email, username
        **password** * 
    """
    try:
        user:user_schema.User = user_service.db_get(
            session=session, email=auth_form.username
        )
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Incorrect credentials"
        )

    if not auth.verify_password(auth_form.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect credentials"
        )

    return auth.tokenize(
        first_name=user.first_name, 
        last_name=user.last_name, 
        email=user.email
    )

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
    response_model=food_schema.Food,
)
def create_food(
    food:food_schema.FoodCreate, 
    session:Session=Depends(get_db),
    token:str = Depends(auth.oauth2_scheme), 
):
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
    response_model=Dict,
)
def delete_food(
    *,
    token:str = Depends(auth.oauth2_scheme),
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
    response_model=food_schema.Food,
)
def update_food(
    *,
    token:str = Depends(auth.oauth2_scheme),
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
    user.hashed_password = auth.hash_password(user.hashed_password)
    return user_service.db_create(session=session, user=user)

@app.post(
    '/users/me', 
    tags=['users'], 
    response_model=user_schema.User
)
def profile(auth_user:user_schema.User=Depends(auth.get_authenticated_user)):
    """Retrieve the authenticated user profile"""
    return auth_user