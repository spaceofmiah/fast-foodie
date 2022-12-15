import logging
from typing import List

from sqlalchemy.orm import Session

from fastapi import FastAPI, Depends

from db.schemas.foods import Food
from db.initializer import get_db
from db.services import foods



app = FastAPI()
logger = logging.getLogger(__name__)


@app.get("/foods", response_model=List[Food])
def list_foods(session:Session=Depends(get_db)):
    """Retrieve all food records"""
    return foods.DQL.list(session=session)

