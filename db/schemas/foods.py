from pydantic import BaseModel
from typing import Union, Sequence


class IngredientBase(BaseModel):
    name: str


class Ingredient(IngredientBase):
    pk: int

    class Config:
        orm_mode: bool = True


class FoodBase(BaseModel):
    name: str
    description: Union[str, None] = None


class Food(FoodBase):
    id: int
    ingredients: Ingredient

    class Config:
        orm_mode: bool = True
