from sqlalchemy.sql import select
from sqlalchemy.orm import Session
from db.initializer import engine

from db.models.foods import Food


class DQL:
    @staticmethod
    def list(session: Session):
        """Handles request to retrieve foods"""
        return session.query(Food).all()
