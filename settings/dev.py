import configparser
import pathlib


# Set application base directory
BASE_DIR = pathlib.Path(".").absolute()

config = configparser.ConfigParser()
config.read(BASE_DIR.joinpath("config.ini"))


# Database connection url
DATABASE_URL = (
    "postgresql+psycopg2://{username}:{password}@{host}:{port}/{db_name}".format(
        host=config["database"]["host"],
        port=config["database"]["port"],
        username=config["database"]["username"],
        password=config["database"]["password"],
        db_name=config["database"]["database_name"],
    )
)


# Application secret key. Should always be kept safe and not to be tracked in
# a public repository
SECRET_KEY = config['app']['secret_key']

# Algorithm to be used in token generation
TOKEN_ALGORITHM = "HS256"

# Total token lifespan in seconds e.g 3600 = 1hr
TOKEN_LIFE_SPAN = 3600

# URL path for which to get token
TOKEN_URL_PATH = "token"

# Account model unique field
USER_UNIQUE_FIELD = "email"
