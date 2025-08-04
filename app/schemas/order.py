from typing import List, Optional
from pydantic import BaseModel
from decimal import Decimal
from app.models.order import OrderStatus, Customer, OrderItem


class CustomerCreate(BaseModel):
    name: str
    phone: str
    address: str


class OrderItemCreate(BaseModel):
    menu_item_id: int
    quantity: int


class OrderCreate(BaseModel):
    customer: CustomerCreate
    items: List[OrderItemCreate]


class OrderStatusUpdate(BaseModel):
    status: OrderStatus


class OrderItemResponse(BaseModel):
    menu_item_id: int
    menu_item_name: str
    quantity: int
    unit_price: Decimal
    item_total: Decimal

    class Config:
        from_attributes = True


class CustomerResponse(BaseModel):
    name: str
    phone: str
    address: str

    class Config:
        from_attributes = True


class OrderResponse(BaseModel):
    id: int
    customer: CustomerResponse
    items: List[OrderItemResponse]
    status: str
    items_total: Decimal
    total_items_count: int

    class Config:
        from_attributes = True


class OrderSummaryResponse(BaseModel):
    id: int
    customer_name: str
    customer_phone: str
    status: str
    items_total: Decimal
    total_items_count: int

    class Config:
        from_attributes = True


class ErrorResponse(BaseModel):
    detail: str
    error_code: Optional[str] = None
