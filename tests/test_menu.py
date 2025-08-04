from fastapi.testclient import TestClient
from app.main import app
from app.schemas.food_item import FoodItemCreate, FoodItemResponse

client = TestClient(app)

def test_create_food_item():
    response = client.post(
        "/menu/",
        json={
            "name": "Pizza",
            "description": "Cheesy pizza with toppings",
            "category": "Main Course",
            "price": 12.99
        }
    )
    assert response.status_code == 201
    assert response.json()["name"] == "Pizza"

def test_read_food_item():
    response = client.get("/menu/1")
    assert response.status_code == 200
    assert response.json()["name"] == "Pizza"

def test_update_food_item():
    response = client.put(
        "/menu/1",
        json={
            "name": "Updated Pizza",
            "description": "Updated cheesy pizza",
            "category": "Main Course",
            "price": 13.99
        }
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Pizza"

def test_delete_food_item():
    response = client.delete("/menu/1")
    assert response.status_code == 204

def test_create_food_item_invalid_price():
    response = client.post(
        "/menu/",
        json={
            "name": "Burger",
            "description": "Delicious beef burger",
            "category": "Main Course",
            "price": -5.00  # Invalid price
        }
    )
    assert response.status_code == 422  # Unprocessable Entity

def test_read_nonexistent_food_item():
    response = client.get("/menu/999")  # Nonexistent ID
    assert response.status_code == 404  # Not Found