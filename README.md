# Restaurant Food Ordering System

This project is a Restaurant Food Ordering System built using FastAPI and Pydantic. It provides a Food Menu Management API that allows users to manage food items in a restaurant's menu.

## Features

- **Food Item Management**: Create, read, update, and delete food items.
- **Category Filtering**: Filter food items by category.
- **Data Validation**: Utilizes Pydantic for data validation and serialization.

## Project Structure

```
restaurant-food-ordering-system
├── app
│   ├── __init__.py
│   ├── main.py
│   ├── models
│   │   ├── __init__.py
│   │   └── food_item.py
│   ├── schemas
│   │   ├── __init__.py
│   │   └── food_item.py
│   ├── api
│   │   ├── __init__.py
│   │   └── endpoints
│   │       ├── __init__.py
│   │       └── menu.py
│   ├── core
│   │   ├── __init__.py
│   │   └── config.py
│   └── database
│       ├── __init__.py
│       └── connection.py
├── tests
│   ├── __init__.py
│   └── test_menu.py
├── requirements.txt
└── README.md
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd restaurant-food-ordering-system
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

- **GET /menu**: Retrieve all food items.
- **POST /menu**: Add a new food item.
- **PUT /menu/{item_id}**: Update an existing food item.
- **DELETE /menu/{item_id}**: Delete a food item.
- **GET /menu/category/{category}**: Retrieve food items by category.

## Testing

To run the tests, use the following command:
```
pytest
```

## License

This project is licensed under the MIT License.