import pytest
from fastapi.testclient import TestClient
from decimal import Decimal
from app.main import app
from app.database.connection import menu_db, orders_db

client = TestClient(app)

@pytest.fixture(autouse=True)
def clear_databases():
    """Clear databases before each test"""
    menu_db.clear()
    orders_db.clear()
    yield
    menu_db.clear()
    orders_db.clear()

@pytest.fixture
def sample_menu_items():
    """Create sample menu items for testing"""
    items = [
        {
            "name": "Margherita Pizza",
            "description": "Classic pizza with tomato sauce, mozzarella cheese, and fresh basil",
            "category": "main_course",
            "price": 15.99,
            "preparation_time": 20,
            "ingredients": ["pizza dough", "tomato sauce", "mozzarella", "basil", "olive oil"],
            "calories": 650,
            "is_vegetarian": True,
            "is_spicy": False
        },
        {
            "name": "Spicy Chicken Wings",
            "description": "Crispy chicken wings tossed in our signature hot sauce",
            "category": "appetizer",
            "price": 12.50,
            "preparation_time": 15,
            "ingredients": ["chicken wings", "hot sauce", "butter", "celery salt"],
            "calories": 420,
            "is_vegetarian": False,
            "is_spicy": True
        }
    ]
    
    created_items = []
    for item in items:
        response = client.post("/menu/", json=item)
        created_items.append(response.json())
    
    return created_items

def test_create_valid_order(sample_menu_items):
    """Test creating a valid order with 2 items and valid customer info"""
    order_data = {
        "customer": {
            "name": "Alice Smith",
            "phone": "5551234567",
            "address": "123 Oak Street, Springfield"
        },
        "items": [
            {
                "menu_item_id": sample_menu_items[0]["id"],  # Margherita Pizza
                "quantity": 1
            },
            {
                "menu_item_id": sample_menu_items[1]["id"],  # Spicy Chicken Wings
                "quantity": 2
            }
        ]
    }
    
    response = client.post("/orders/", json=order_data)
    assert response.status_code == 201
    
    data = response.json()
    assert data["customer"]["name"] == "Alice Smith"
    assert len(data["items"]) == 2
    assert data["items"][0]["quantity"] == 1
    assert data["items"][1]["quantity"] == 2
    
    # Check calculated totals
    expected_total = Decimal("15.99") + (Decimal("12.50") * 2)  # Pizza + 2x Wings
    assert Decimal(str(data["items_total"])) == expected_total
    assert data["total_items_count"] == 3  # 1 pizza + 2 wings
    assert data["status"] == "pending"

def test_empty_items_order():
    """Test creating order with no items (should fail)"""
    order_data = {
        "customer": {
            "name": "Bob Johnson",
            "phone": "5551234567",
            "address": "456 Pine Street, Springfield"
        },
        "items": []  # Empty items list
    }
    
    response = client.post("/orders/", json=order_data)
    assert response.status_code == 422

def test_invalid_phone_order():
    """Test creating order with invalid phone number"""
    order_data = {
        "customer": {
            "name": "Charlie Brown",
            "phone": "123",  # Invalid phone
            "address": "789 Elm Street, Springfield"
        },
        "items": [
            {
                "menu_item_id": 1,
                "quantity": 1
            }
        ]
    }
    
    response = client.post("/orders/", json=order_data)
    assert response.status_code == 422

def test_large_quantity_order(sample_menu_items):
    """Test ordering large quantity (should fail as max is 10)"""
    order_data = {
        "customer": {
            "name": "David Wilson",
            "phone": "5551234567",
            "address": "321 Maple Street, Springfield"
        },
        "items": [
            {
                "menu_item_id": sample_menu_items[0]["id"],
                "quantity": 15  # Exceeds max of 10
            }
        ]
    }
    
    response = client.post("/orders/", json=order_data)
    assert response.status_code == 422

def test_nonexistent_menu_item():
    """Test ordering non-existent menu item"""
    order_data = {
        "customer": {
            "name": "Eve Davis",
            "phone": "5551234567",
            "address": "654 Cedar Street, Springfield"
        },
        "items": [
            {
                "menu_item_id": 999,  # Non-existent item
                "quantity": 1
            }
        ]
    }
    
    response = client.post("/orders/", json=order_data)
    assert response.status_code == 404

def test_get_all_orders(sample_menu_items):
    """Test getting all orders"""
    # Create a few orders first
    orders = [
        {
            "customer": {
                "name": "Alice Smith",
                "phone": "5551234567",
                "address": "123 Oak Street, Springfield"
            },
            "items": [
                {
                    "menu_item_id": sample_menu_items[0]["id"],
                    "quantity": 1
                }
            ]
        },
        {
            "customer": {
                "name": "Bob Johnson",
                "phone": "5559876543",
                "address": "456 Pine Street, Springfield"
            },
            "items": [
                {
                    "menu_item_id": sample_menu_items[1]["id"],
                    "quantity": 3
                }
            ]
        }
    ]
    
    for order in orders:
        client.post("/orders/", json=order)
    
    # Get all orders
    response = client.get("/orders/")
    assert response.status_code == 200
    
    data = response.json()
    assert len(data) == 2

def test_get_order_by_id(sample_menu_items):
    """Test getting specific order by ID"""
    # Create an order
    order_data = {
        "customer": {
            "name": "Charlie Brown",
            "phone": "5551234567",
            "address": "789 Elm Street, Springfield"
        },
        "items": [
            {
                "menu_item_id": sample_menu_items[0]["id"],
                "quantity": 2
            }
        ]
    }
    
    create_response = client.post("/orders/", json=order_data)
    created_order = create_response.json()
    order_id = created_order["id"]
    
    # Get order by ID
    response = client.get(f"/orders/{order_id}")
    assert response.status_code == 200
    
    data = response.json()
    assert data["customer"]["name"] == "Charlie Brown"
    assert len(data["items"]) == 1
    assert data["items"][0]["quantity"] == 2

def test_get_nonexistent_order():
    """Test getting non-existent order"""
    response = client.get("/orders/999")
    assert response.status_code == 404

def test_status_update_valid_transition(sample_menu_items):
    """Test updating order status with valid transition"""
    # Create an order
    order_data = {
        "customer": {
            "name": "Frank Miller",
            "phone": "5551234567",
            "address": "987 Birch Street, Springfield"
        },
        "items": [
            {
                "menu_item_id": sample_menu_items[0]["id"],
                "quantity": 1
            }
        ]
    }
    
    create_response = client.post("/orders/", json=order_data)
    created_order = create_response.json()
    order_id = created_order["id"]
    
    # Update status from pending to confirmed
    update_data = {"status": "confirmed"}
    response = client.put(f"/orders/{order_id}/status", json=update_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "confirmed"

def test_status_update_invalid_transition(sample_menu_items):
    """Test updating order status with invalid transition"""
    # Create an order
    order_data = {
        "customer": {
            "name": "Grace Lee",
            "phone": "5551234567",
            "address": "147 Spruce Street, Springfield"
        },
        "items": [
            {
                "menu_item_id": sample_menu_items[0]["id"],
                "quantity": 1
            }
        ]
    }
    
    create_response = client.post("/orders/", json=order_data)
    created_order = create_response.json()
    order_id = created_order["id"]
    
    # Try to update status from pending directly to delivered (invalid)
    update_data = {"status": "delivered"}
    response = client.put(f"/orders/{order_id}/status", json=update_data)
    assert response.status_code == 400

def test_status_update_nonexistent_order():
    """Test updating status of non-existent order"""
    update_data = {"status": "confirmed"}
    response = client.put("/orders/999/status", json=update_data)
    assert response.status_code == 404

def test_order_total_calculation(sample_menu_items):
    """Test that order totals are calculated correctly"""
    order_data = {
        "customer": {
            "name": "Henry Ford",
            "phone": "5551234567",
            "address": "258 Walnut Street, Springfield"
        },
        "items": [
            {
                "menu_item_id": sample_menu_items[0]["id"],  # Pizza $15.99
                "quantity": 2
            },
            {
                "menu_item_id": sample_menu_items[1]["id"],  # Wings $12.50
                "quantity": 1
            }
        ]
    }
    
    response = client.post("/orders/", json=order_data)
    assert response.status_code == 201
    
    data = response.json()
    
    # Check individual item totals
    assert Decimal(str(data["items"][0]["item_total"])) == Decimal("15.99") * 2
    assert Decimal(str(data["items"][1]["item_total"])) == Decimal("12.50") * 1
    
    # Check overall total
    expected_total = (Decimal("15.99") * 2) + (Decimal("12.50") * 1)
    assert Decimal(str(data["items_total"])) == expected_total
    
    # Check item count
    assert data["total_items_count"] == 3  # 2 pizzas + 1 wings
