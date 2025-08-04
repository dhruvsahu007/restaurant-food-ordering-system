from pydantic import BaseModel, Field, constr, condecimal
from typing import Optional

class FoodItemBase(BaseModel):
    name: constr(min_length=1, max_length=100) = Field(..., description="The name of the food item")
    description: Optional[constr(max_length=500)] = Field(None, description="A brief description of the food item")
    category: constr(min_length=1, max_length=50) = Field(..., description="The category of the food item (e.g., appetizer, main course, dessert)")
    price: condecimal(gt=0) = Field(..., description="The price of the food item, must be greater than zero")

class FoodItemCreate(FoodItemBase):
    pass

class FoodItemUpdate(FoodItemBase):
    pass

class FoodItemResponse(FoodItemBase):
    id: int = Field(..., description="The unique identifier for the food item")

    class Config:
        orm_mode = True