from sqlalchemy.orm import Session
from db.models import users


def db_list(session:Session):
	return session.query(users.User).all()