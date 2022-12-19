import logging
from typing import List, Dict

from sqlalchemy.orm import Session

from fastapi import (
    HTTPException,
    APIRouter, 
    FastAPI, 
    Depends, 
    status
)
from fastapi.security import OAuth2PasswordRequestForm
from db.services import users as user_db_services
from db.schemas import users as user_schema
from settings.dev import TOKEN_URL_PATH
from db.initializer import get_db
from utils import auth


router = APIRouter()

logger = logging.getLogger(__name__)


@router.post(f"/{TOKEN_URL_PATH}", tags=["auth"], response_model=Dict[str, str])
def login(
    auth_form:OAuth2PasswordRequestForm=Depends(), 
    session:Session=Depends(get_db),
):
    """Processes user's authentication request

        **username** * : Unique identifier e.g email, username

        **password** * 
    """
    try:
        user:user_schema.User = user_db_services.db_get(
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