import os
import pathlib


# Set application base directory
BASE_DIR = pathlib.Path(".").absolute()


# Database connection url
DATABASE_URL = (
    "postgresql+psycopg2://{username}:{password}@{host}:{port}/{db_name}".format(
        host=os.environ.get("DATABASE_HOST"),
        port=os.environ.get("DATABASE_PORT"),
        db_name=os.environ.get("DATABASE_NAME"),
        username=os.environ.get("DATABASE_USER"),
        password=os.environ.get("DATABASE_PASS"),
    )
)


# Application secret key. Should always be kept safe and not to be tracked in
# a public repository
SECRET_KEY = os.environ.get('SECRET_KEY')

# Algorithm to be used in token generation
TOKEN_ALGORITHM = "HS256"

# Total token lifespan in seconds e.g 3600 = 1hr
TOKEN_LIFE_SPAN = 3600

# URL path for which to get token
TOKEN_URL_PATH = "token"

# Account model unique field
USER_UNIQUE_FIELD = "email"
