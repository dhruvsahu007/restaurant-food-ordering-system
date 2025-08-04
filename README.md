# Restaurant Ordering System

This project is a Restaurant Ordering System built using FastAPI and Pydantic. It provides a comprehensive API for managing both restaurant menu items and customer orders with nested models.

## Features

- **Food Menu Management**: Create, read, update, and delete food items
- **Order Management**: Create and manage customer orders with nested customer and item data
- **Status Tracking**: Track order status from pending to delivered
- **Data Validation**: Comprehensive validation using Pydantic models
- **Nested Models**: Demonstrates relationships between customers, orders, and menu items

## Project Structure

```
restaurant-ordering-system
├── app
│   ├── __init__.py
│   ├── main.py
│   ├── models
│   │   ├── __init__.py
│   │   ├── food_item.py
│   │   └── order.py          # New: Order, Customer, OrderItem models
│   ├── schemas
│   │   ├── __init__.py
│   │   ├── food_item.py
│   │   └── order.py          # New: Order request/response schemas
│   ├── api
│   │   ├── __init__.py
│   │   └── endpoints
│   │       ├── __init__.py
│   │       ├── menu.py
│   │       └── orders.py     # New: Order management endpoints
│   ├── core
│   │   ├── __init__.py
│   │   └── config.py
│   └── database
│       ├── __init__.py
│       └── connection.py     # Updated: Added order database functions
├── tests
│   ├── __init__.py
│   ├── test_menu.py
│   └── test_orders.py        # New: Comprehensive order tests
├── requirements.txt
└── README.md
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd restaurant-ordering-system
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

To run the application, execute the following command:
```
uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

## API Endpoints

### Menu Endpoints
- **GET /menu**: Retrieve all food items
- **POST /menu**: Add a new food item
- **PUT /menu/{item_id}**: Update an existing food item
- **DELETE /menu/{item_id}**: Delete a food item
- **GET /menu/category/{category}**: Retrieve food items by category

### Order Endpoints
- **POST /orders**: Create a new order with customer info and items
- **GET /orders**: Retrieve all orders (summary view)
- **GET /orders/{order_id}**: Retrieve specific order details
- **PUT /orders/{order_id}/status**: Update order status

## Nested Models

### Order Model Structure
```python
Order {
    id: int
    customer: Customer {
        name: str
        phone: str
        address: str
    }
    items: List[OrderItem] {
        menu_item_id: int
        menu_item_name: str
        quantity: int
        unit_price: Decimal
        item_total: Decimal (computed)
    }
    status: OrderStatus (pending, confirmed, ready, delivered)
    items_total: Decimal (computed)
    total_items_count: int (computed)
}
```

## Sample API Usage

### Create an Order
```bash
curl -X POST "http://127.0.0.1:8000/orders/" \
     -H "Content-Type: application/json" \
     -d '{
       "customer": {
         "name": "Alice Smith",
         "phone": "5551234567",
         "address": "123 Oak Street, Springfield"
       },
       "items": [
         {
           "menu_item_id": 1,
           "quantity": 2
         },
         {
           "menu_item_id": 2,
           "quantity": 1
         }
       ]
     }'
```

### Update Order Status
```bash
curl -X PUT "http://127.0.0.1:8000/orders/1/status" \
     -H "Content-Type: application/json" \
     -d '{"status": "confirmed"}'
```

## Testing

To run the tests, use the following command:
```
pytest
```

The test suite includes:
- Menu item management tests
- Order creation and validation tests
- Nested model validation tests
- Status transition tests
- Error handling tests

## Validation Features

- **Customer Validation**: Name format, phone number format, address length
- **Order Item Validation**: Quantity limits, menu item existence
- **Status Transitions**: Enforced order status workflow
- **Business Rules**: Computed totals, item availability checks

## License

This project is licensed under the MIT License.