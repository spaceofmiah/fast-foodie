from sqlalchemy import update, select
from sqlalchemy.orm import Session
from db.initializer import engine

from db.models import foods as food_model
from db.schemas.foods import FoodCreate, FoodUpdate



def db_list(session: Session):
    """Handles request to retrieve foods"""
    return session.query(food_model.Food).all()

def db_get(session: Session, food_id:int):
    """Retrieve a food instance"""
    return session.query(food_model.Food).filter(food_model.Food.id==food_id).one()

def db_delete(session: Session, food_id:int):
    """Delete a unique food instance"""
    food = db_get(session, food_id=food_id)
    session.delete(food)
    session.commit()

def db_create(session:Session, food:FoodCreate):
    """Creates new food instance"""
    db_food = food_model.Food(
        name=food.name, 
        description=food.description
    )
    session.add(db_food)
    session.commit()
    session.refresh(db_food)
    return db_food

def db_update(session: Session, food_id: int, food:FoodUpdate):
    """Updates an existing food instance"""
    statement = (
        update(food_model.Food)
        .where(food_model.Food.id == food_id)
        .values(
            name=food.name,
            description=food.description
        )
        .execution_options(populate_existing=True)
    )
    session.execute(statement)
    return session.commit()



