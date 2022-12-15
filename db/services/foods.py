from sqlalchemy.orm import Session
from db.initializer import engine

from db.models import foods as food_model
from db.schemas.foods import FoodCreate



def list(session: Session):
    """Handles request to retrieve foods"""
    return session.query(food_model.Food).all()

def create(session:Session, food:FoodCreate):
    db_food = food_model.Food(
        name=food.name, 
        description=food.description
    )
    session.add(db_food)
    session.commit()
    session.refresh(db_food)
    return db_food



