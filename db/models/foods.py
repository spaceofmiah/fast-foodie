from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey

from db.initializer import Base


class Food(Base):
    """
    Models a database table named Food
    """

    __tablename__ = "foods"

    id = Column(Integer, primary_key=True)
    name = Column(String(225), nullable=False)
    description = Column(String, nullable=True)

    ingredients = relationship("Ingredient", back_populates="food")

    def __repr__(self) -> str:
        return f"Food({self.name!r})"


class Ingredient(Base):
    """
    Models a database table named Ingredient.
    """

    __tablename__ = "ingredients"

    pk = Column(Integer, primary_key=True)
    name = Column(String(225), nullable=False)

    food_id = Column(Integer, ForeignKey("foods.id"), nullable=False)
    food = relationship("Food", back_populates="ingredients")

    def __repr__(self) -> str:
        return f"Ingredient({self.name!r})"
