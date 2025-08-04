from typing import Dict, Any

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