from sqlalchemy.sql import select
from sqlalchemy.orm import Session
from db.initializer import engine

from ..models.foods import Food, Ingredient
from ..schemas.food_schemas import Food as FoodSchema


class DQL:
    @staticmethod
    def retrieve_foods():
        """Handles request to retrieve foods"""
        with engine.connect() as conn:
            return conn.execute(select(Food))
