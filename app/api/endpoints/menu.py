from fastapi import APIRouter, HTTPException
from typing import List, Optional
from app.models.food_item import FoodItem
from app.schemas.food_item import FoodItemCreate, FoodItemUpdate

router = APIRouter()

menu_db = {}

@router.post("/menu/", response_model=FoodItem)
def create_food_item(food_item: FoodItemCreate):
    item_id = len(menu_db) + 1
    new_item = FoodItem(id=item_id, **food_item.dict())
    menu_db[item_id] = new_item
    return new_item

@router.get("/menu/", response_model=List[FoodItem])
def get_food_items(category: Optional[str] = None):
    if category:
        return [item for item in menu_db.values() if item.category == category]
    return list(menu_db.values())

@router.get("/menu/{item_id}", response_model=FoodItem)
def get_food_item(item_id: int):
    if item_id not in menu_db:
        raise HTTPException(status_code=404, detail="Food item not found")
    return menu_db[item_id]

@router.put("/menu/{item_id}", response_model=FoodItem)
def update_food_item(item_id: int, food_item: FoodItemUpdate):
    if item_id not in menu_db:
        raise HTTPException(status_code=404, detail="Food item not found")
    updated_item = menu_db[item_id].copy(update=food_item.dict())
    menu_db[item_id] = updated_item
    return updated_item

@router.delete("/menu/{item_id}", response_model=dict)
def delete_food_item(item_id: int):
    if item_id not in menu_db:
        raise HTTPException(status_code=404, detail="Food item not found")
    del menu_db[item_id]
    return {"message": "Food item deleted successfully"}