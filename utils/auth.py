import datetime
import bcrypt
import jwt

from sqlalchemy.orm import Session

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from db.initializer import get_db
from db.schemas import users as schema
from db.services import users as db_service
from settings.dev import (
	SECRET_KEY, 
	TOKEN_ALGORITHM, 
	TOKEN_LIFE_SPAN, 
	TOKEN_URL_PATH, 
	USER_UNIQUE_FIELD
)



oauth2_scheme = OAuth2PasswordBearer(tokenUrl=TOKEN_URL_PATH)



def issue_token_lifespan() -> dict:
	"""Create token lifespan"""
	issue_time = datetime.datetime.now(tz=datetime.timezone.utc)
	expiration_time = issue_time  + datetime.timedelta(seconds=TOKEN_LIFE_SPAN)
	return {"iat": issue_time, "exp": expiration_time}

def hash_password(password):
	return bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())

def verify_password(password, hashed_password):
	return bcrypt.checkpw(password.encode('utf8'), hashed_password)

def tokenize(first_name:str, last_name:str, email:str) -> dict:
	"""Tokenizes user data"""
	data = {
		**issue_token_lifespan(),
		"first_name": first_name,
		"last_name": last_name,
		"email": email,
	}
	token = jwt.encode(data, SECRET_KEY, algorithm=TOKEN_ALGORITHM)
	return {'access_token': token, 'token_type': 'bearer'}

def detokenize(token:str) -> dict:
	"""Returns payload from a token"""
	return jwt.decode(token, SECRET_KEY, algorithms=[TOKEN_ALGORITHM])

def get_authenticated_user(
	token:str = Depends(oauth2_scheme), 
	session:Session=Depends(get_db)
) -> schema.User :
	"""Retrieve authenticated user from token"""
	payload = detokenize(token)
	assert USER_UNIQUE_FIELD in payload, "Invalid token"
	return db_service.db_get(session=session, email=payload['email'])





