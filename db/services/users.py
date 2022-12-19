from sqlalchemy.orm import Session

from db.models import users
from db.schemas import users as schema


def db_list(session:Session):
	return session.query(users.User).all()

def db_create(session:Session, user=schema.UserCreate):
	"""Handles creation of a user in the database"""
	db_user = users.User(**user.dict())
	session.add(db_user)
	session.commit()
	session.refresh(db_user)
	return db_user