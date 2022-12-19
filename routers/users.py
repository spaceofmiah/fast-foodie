from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from db.initializer import get_db
from db.schemas import users as schema
from db.services import users as db_service

from utils import auth



router = APIRouter()



@router.get('/users', tags=['users'], response_model=List[schema.User])
def list(session:Session=Depends(get_db)):
    """Retrieves all available users"""
    return db_service.db_list(session)

@router.post('/users', tags=['users'], response_model=schema.User)
def create(
    *,
    session:Session=Depends(get_db), 
    user:schema.UserCreate
):
    """Create a new user

        **first_name** : first name of the user to be created

        **last_name**  : last name of the user to be created

        **email** * : unique email address of user

        **password**   : user's password
    """
    user.hashed_password = auth.hash_password(user.hashed_password)
    return db_service.db_create(session=session, user=user)

@router.get(
    '/users/me', 
    tags=['users'], 
    response_model=schema.User
)
def profile(auth_user:schema.User=Depends(auth.get_authenticated_user)):
    """Retrieve the authenticated user profile"""
    return auth_user