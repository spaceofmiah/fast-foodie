from fastapi.testclient import TestClient
from src.main import app


client = TestClient(app)


def test_food_listings_returns_data(mocker):
    """Ensure that food is listed on request"""

    mocker.patch("src.main.food_db", ["Food 1", "Food 2", "Food 3"])

    # Make request to retrieve all foods
    res = client.get("/foods")

    # Ensure that the request is successful
    assert res.status_code == 200

    # Ensure that the result returned is accurate
    assert len(res.json()["results"]) == 3


def test_food_is_retrieved_given_its_id(mocker):
    """Ensure an appropriate food is retrieved given the food id"""

    mocker.patch("src.main.food_db", ["Food 1", "Food 2", "Food 3"])

    # Make request to retrieve all foods
    res = client.get("/foods/1")

    # Ensure that the request is successful
    assert res.status_code == 200

    # Ensure the right food is what's returned
    assert res.json() == "Food 2"
