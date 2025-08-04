from typing import Dict, Any
from app.models.food_item import FoodItem
from app.models.order import Order

# In-memory databases using dictionaries
menu_db: Dict[int, FoodItem] = {}
orders_db: Dict[int, Order] = {}

# Auto-incrementing IDs
next_menu_id = 1
next_order_id = 1


# Menu Database Functions
def get_next_menu_id() -> int:
    """Generate next available menu ID"""
    global next_menu_id
    if not menu_db:
        next_menu_id = 1
    else:
        next_menu_id = max(menu_db.keys()) + 1
    return next_menu_id


def add_item(item: FoodItem) -> FoodItem:
    """Add item to menu database"""
    if item.id is None:
        item.id = get_next_menu_id()
    menu_db[item.id] = item
    return item


def get_item(item_id: int) -> FoodItem:
    """Get menu item by ID"""
    return menu_db.get(item_id)


def get_all_items() -> Dict[int, FoodItem]:
    """Get all menu items"""
    return menu_db


def update_item(item_id: int, item: FoodItem) -> FoodItem:
    """Update menu item in database"""
    if item_id in menu_db:
        item.id = item_id
        menu_db[item_id] = item
        return item
    return None


def delete_item(item_id: int) -> bool:
    """Delete menu item from database"""
    if item_id in menu_db:
        del menu_db[item_id]
        return True
    return False


def get_items_by_category(category: str) -> Dict[int, FoodItem]:
    """Get menu items by category"""
    return {k: v for k, v in menu_db.items() if v.category == category}


# Order Database Functions
def get_next_order_id() -> int:
    """Generate next available order ID"""
    global next_order_id
    if not orders_db:
        next_order_id = 1
    else:
        next_order_id = max(orders_db.keys()) + 1
    return next_order_id


def add_order(order: Order) -> Order:
    """Add order to database"""
    if order.id is None:
        order.id = get_next_order_id()
    orders_db[order.id] = order
    return order


def get_order(order_id: int) -> Order:
    """Get order by ID"""
    return orders_db.get(order_id)


def get_all_orders() -> Dict[int, Order]:
    """Get all orders"""
    return orders_db


def update_order(order_id: int, order: Order) -> Order:
    """Update order in database"""
    if order_id in orders_db:
        order.id = order_id
        orders_db[order_id] = order
        return order
    return None


def update_order_status(order_id: int, status: str) -> Order:
    """Update order status"""
    if order_id in orders_db:
        orders_db[order_id].status = status
        return orders_db[order_id]
    return None

class Database:
    def __init__(self):
        self.menu_db: Dict[int, Dict[str, Any]] = {}
        self.current_id: int = 1

    def add_item(self, item: Dict[str, Any]) -> int:
        item_id = self.current_id
        self.menu_db[item_id] = item
        self.current_id += 1
        return item_id

    def get_item(self, item_id: int) -> Dict[str, Any]:
        return self.menu_db.get(item_id)

    def update_item(self, item_id: int, item: Dict[str, Any]) -> bool:
        if item_id in self.menu_db:
            self.menu_db[item_id] = item
            return True
        return False

    def delete_item(self, item_id: int) -> bool:
        if item_id in self.menu_db:
            del self.menu_db[item_id]
            return True
        return False

    def get_all_items(self) -> Dict[int, Dict[str, Any]]:
        return self.menu_db

    def filter_by_category(self, category: str) -> Dict[int, Dict[str, Any]]:
        return {item_id: item for item_id, item in self.menu_db.items() if item.get('category') == category}