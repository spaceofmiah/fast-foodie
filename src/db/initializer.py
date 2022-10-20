from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from settings.dev import DATABASE_URL


# Create Engine
engine = create_engine(DATABASE_URL, echo=True, future=True)

Base = declarative_base()


def create_connection():
    """Returns database engine connection"""
    return engine.connect()

