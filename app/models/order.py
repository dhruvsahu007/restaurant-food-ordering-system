from enum import Enum
from typing import List
from pydantic import BaseModel, Field, validator
from decimal import Decimal


class OrderStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    READY = "ready"
    DELIVERED = "delivered"


class Customer(BaseModel):
    """Simple nested customer model for items in order"""
    name: str = Field(..., min_length=2, max_length=50)
    phone: str = Field(..., pattern=r"^\+?\d{10}$")
    address: str = Field(..., min_length=5, max_length=200)

    @validator('name')
    def validate_name(cls, v):
        if not v.replace(' ', '').isalpha():
            raise ValueError('Name should contain only letters and spaces')
        return v


class OrderItem(BaseModel):
    """Simple nested model for items in order"""
    menu_item_id: int = Field(..., gt=0)
    menu_item_name: str = Field(..., min_length=1, max_length=100)  # Store name for easy access
    quantity: int = Field(..., gt=0, le=10)
    unit_price: Decimal = Field(..., gt=0, max_digits=6, decimal_places=2)

    @property
    def item_total(self) -> Decimal:
        return self.quantity * self.unit_price


class Order(BaseModel):
    """Order model with nested Customer and OrderItem models"""
    id: int = None
    customer: Customer
    items: List[OrderItem] = Field(..., min_items=1)
    status: OrderStatus = OrderStatus.PENDING
    
    @property
    def items_total(self) -> Decimal:
        """Calculate total amount for all items"""
        return sum(item.item_total for item in self.items)
    
    @property
    def total_items_count(self) -> int:
        """Calculate total number of items"""
        return sum(item.quantity for item in self.items)

    class Config:
        use_enum_values = True
