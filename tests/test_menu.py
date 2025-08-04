import pytest
from fastapi.testclient import TestClient
from decimal import Decimal
from app.main import app
from app.database.connection import menu_db

client = TestClient(app)

@pytest.fixture(autouse=True)
def clear_database():
    """Clear database before each test"""
    menu_db.clear()
    yield
    menu_db.clear()

def test_create_valid_food_item():
    """Test creating a valid food item"""
    item_data = {
        "name": "Margherita Pizza",
        "description": "Classic pizza with tomato sauce, mozzarella cheese, and fresh basil",
        "category": "main_course",
        "price": 15.99,
        "preparation_time": 20,
        "ingredients": ["pizza dough", "tomato sauce", "mozzarella", "basil", "olive oil"],
        "calories": 650,
        "is_vegetarian": True,
        "is_spicy": False
    }
    
    response = client.post("/menu/", json=item_data)
    assert response.status_code == 201
    
    data = response.json()
    assert data["name"] == "Margherita Pizza"
    assert data["price_category"] == "Mid-range"
    assert "Vegetarian" in data["dietary_info"]

def test_invalid_price():
    """Test creating item with invalid price"""
    item_data = {
        "name": "Cheap Item",
        "description": "Very cheap item for testing",
        "category": "appetizer",
        "price": 0.50,  # Invalid: below $1.00
        "preparation_time": 10,
        "ingredients": ["ingredient1"]
    }
    
    response = client.post("/menu/", json=item_data)
    assert response.status_code == 422

def test_spicy_beverage_validation():
    """Test that beverages cannot be marked as spicy"""
    item_data = {
        "name": "Hot Coffee",
        "description": "A very hot coffee beverage",
        "category": "beverage",
        "price": 3.99,
        "preparation_time": 5,
        "ingredients": ["coffee beans", "water"],
        "is_spicy": True  # Invalid: beverages cannot be spicy
    }
    
    response = client.post("/menu/", json=item_data)
    assert response.status_code == 422

def test_invalid_name():
    """Test creating item with invalid name"""
    item_data = {
        "name": "Pizza123!",  # Invalid: contains numbers and special characters
        "description": "Pizza with invalid name",
        "category": "main_course",
        "price": 12.99,
        "preparation_time": 20,
        "ingredients": ["ingredient1"]
    }
    
    response = client.post("/menu/", json=item_data)
    assert response.status_code == 422

def test_empty_ingredients():
    """Test creating item with empty ingredients list"""
    item_data = {
        "name": "Empty Dish",
        "description": "Dish with no ingredients",
        "category": "appetizer",
        "price": 5.99,
        "preparation_time": 10,
        "ingredients": []  # Invalid: at least 1 ingredient required
    }
    
    response = client.post("/menu/", json=item_data)
    assert response.status_code == 422

def test_get_all_items():
    """Test getting all menu items"""
    # First create an item
    item_data = {
        "name": "Test Item",
        "description": "Test item for getting all items",
        "category": "appetizer",
        "price": 8.99,
        "preparation_time": 15,
        "ingredients": ["test ingredient"]
    }
    
    client.post("/menu/", json=item_data)
    
    # Get all items
    response = client.get("/menu/")
    assert response.status_code == 200
    
    data = response.json()
    assert len(data) == 1

def test_get_item_by_id():
    """Test getting specific item by ID"""
    # Create an item
    item_data = {
        "name": "Specific Item",
        "description": "Item to test getting by ID",
        "category": "main_course",
        "price": 12.99,
        "preparation_time": 25,
        "ingredients": ["ingredient1", "ingredient2"]
    }
    
    create_response = client.post("/menu/", json=item_data)
    created_item = create_response.json()
    item_id = created_item["id"]
    
    # Get item by ID
    response = client.get(f"/menu/{item_id}")
    assert response.status_code == 200
    
    data = response.json()
    assert data["name"] == "Specific Item"

def test_update_item():
    """Test updating an existing item"""
    # Create an item
    item_data = {
        "name": "Original Item",
        "description": "Original description",
        "category": "appetizer",
        "price": 6.99,
        "preparation_time": 10,
        "ingredients": ["ingredient1"]
    }
    
    create_response = client.post("/menu/", json=item_data)
    created_item = create_response.json()
    item_id = created_item["id"]
    
    # Update the item
    update_data = {
        "name": "Updated Item",
        "price": 8.99
    }
    
    response = client.put(f"/menu/{item_id}", json=update_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["name"] == "Updated Item"
    assert data["price"] == 8.99

def test_delete_item():
    """Test deleting an item"""
    # Create an item
    item_data = {
        "name": "Item to Delete",
        "description": "This item will be deleted",
        "category": "dessert",
        "price": 4.99,
        "preparation_time": 5,
        "ingredients": ["ingredient1"]
    }
    
    create_response = client.post("/menu/", json=item_data)
    created_item = create_response.json()
    item_id = created_item["id"]
    
    # Delete the item
    response = client.delete(f"/menu/{item_id}")
    assert response.status_code == 204
    
    # Verify item is deleted
    get_response = client.get(f"/menu/{item_id}")
    assert get_response.status_code == 404

def test_get_items_by_category():
    """Test getting items by category"""
    # Create items in different categories
    items = [
        {
            "name": "Appetizer Item",
            "description": "Test appetizer",
            "category": "appetizer",
            "price": 6.99,
            "preparation_time": 10,
            "ingredients": ["ingredient1"]
        },
        {
            "name": "Main Course Item",
            "description": "Test main course",
            "category": "main_course",
            "price": 16.99,
            "preparation_time": 30,
            "ingredients": ["ingredient1", "ingredient2"]
        }
    ]
    
    for item in items:
        client.post("/menu/", json=item)
    
    # Get appetizers only
    response = client.get("/menu/category/appetizer")
    assert response.status_code == 200
    
    data = response.json()
    assert len(data) == 1
    
    # Check that all returned items are appetizers
    for item in data.values():
        assert item["category"] == "appetizer"

def test_read_nonexistent_food_item():
    """Test reading a non-existent food item"""
    response = client.get("/menu/999")
    assert response.status_code == 404
