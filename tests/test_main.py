from fastapi.testclient import TestClient
from main import app


client = TestClient(app)


def test_food_listings_returns_data(mocker):
    """Ensure that food is listed on request"""
    pass


def test_food_is_retrieved_given_its_id(mocker):
    """Ensure an appropriate food is retrieved given the food id"""
    pass