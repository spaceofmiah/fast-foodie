import configparser
import pathlib


# Set application base directory
BASE_DIR = pathlib.Path('.').absolute()

config = configparser.ConfigParser()
config.read(BASE_DIR.joinpath('config.ini'))



DATABASE_URL = "postgresql+psycopg2://{username}:{password}@{host}:{port}/{db_name}".format(
	host=config['database']['host'],
	port=config['database']['port'],
	username=config['database']['username'],
	password=config['database']['password'],
	db_name=config['database']['database_name'],
)