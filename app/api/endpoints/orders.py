from typing import Dict, List
from fastapi import APIRouter, HTTPException, status
from app.models.order import Order, OrderItem, OrderStatus
from app.schemas.order import (
    OrderCreate, OrderResponse, OrderSummaryResponse, 
    OrderStatusUpdate, OrderItemResponse, CustomerResponse, ErrorResponse
)
from app.database.connection import (
    add_order, get_order, get_all_orders, update_order_status,
    get_item  # To validate menu items exist
)

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(order_data: OrderCreate):
    """Create new order"""
    try:
        # Validate that all menu items exist and build order items
        order_items = []
        for item_data in order_data.items:
            menu_item = get_item(item_data.menu_item_id)
            if not menu_item:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Menu item with ID {item_data.menu_item_id} not found"
                )
            
            if not menu_item.is_available:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Menu item '{menu_item.name}' is not available"
                )
            
            order_item = OrderItem(
                menu_item_id=item_data.menu_item_id,
                menu_item_name=menu_item.name,
                quantity=item_data.quantity,
                unit_price=menu_item.price
            )
            order_items.append(order_item)
        
        # Create order instance for validation
        order = Order(
            customer=order_data.customer,
            items=order_items
        )
        
        # Add to database
        created_order = add_order(order)
        
        # Build response
        response_items = [
            OrderItemResponse(
                menu_item_id=item.menu_item_id,
                menu_item_name=item.menu_item_name,
                quantity=item.quantity,
                unit_price=item.unit_price,
                item_total=item.item_total
            ) for item in created_order.items
        ]
        
        return OrderResponse(
            id=created_order.id,
            customer=CustomerResponse(
                name=created_order.customer.name,
                phone=created_order.customer.phone,
                address=created_order.customer.address
            ),
            items=response_items,
            status=created_order.status,
            items_total=created_order.items_total,
            total_items_count=created_order.total_items_count
        )
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e)
        )


@router.get("/", response_model=Dict[int, OrderSummaryResponse])
async def get_all_orders_endpoint():
    """Get all orders with summary information"""
    orders = get_all_orders()
    return {
        k: OrderSummaryResponse(
            id=v.id,
            customer_name=v.customer.name,
            customer_phone=v.customer.phone,
            status=v.status,
            items_total=v.items_total,
            total_items_count=v.total_items_count
        ) for k, v in orders.items()
    }


@router.get("/{order_id}", response_model=OrderResponse)
async def get_order_details(order_id: int):
    """Get specific order details"""
    order = get_order(order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order with ID {order_id} not found"
        )
    
    # Build response
    response_items = [
        OrderItemResponse(
            menu_item_id=item.menu_item_id,
            menu_item_name=item.menu_item_name,
            quantity=item.quantity,
            unit_price=item.unit_price,
            item_total=item.item_total
        ) for item in order.items
    ]
    
    return OrderResponse(
        id=order.id,
        customer=CustomerResponse(
            name=order.customer.name,
            phone=order.customer.phone,
            address=order.customer.address
        ),
        items=response_items,
        status=order.status,
        items_total=order.items_total,
        total_items_count=order.total_items_count
    )


@router.put("/{order_id}/status", response_model=OrderResponse)
async def update_order_status_endpoint(order_id: int, status_data: OrderStatusUpdate):
    """Update order status"""
    order = get_order(order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order with ID {order_id} not found"
        )
    
    # Validate status transition (basic validation)
    current_status = OrderStatus(order.status)
    new_status = status_data.status
    
    # Basic status transition validation
    valid_transitions = {
        OrderStatus.PENDING: [OrderStatus.CONFIRMED],
        OrderStatus.CONFIRMED: [OrderStatus.READY],
        OrderStatus.READY: [OrderStatus.DELIVERED],
        OrderStatus.DELIVERED: []  # Final state
    }
    
    if new_status not in valid_transitions.get(current_status, []):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot transition from {current_status} to {new_status}"
        )
    
    # Update status
    updated_order = update_order_status(order_id, new_status.value)
    
    # Build response
    response_items = [
        OrderItemResponse(
            menu_item_id=item.menu_item_id,
            menu_item_name=item.menu_item_name,
            quantity=item.quantity,
            unit_price=item.unit_price,
            item_total=item.item_total
        ) for item in updated_order.items
    ]
    
    return OrderResponse(
        id=updated_order.id,
        customer=CustomerResponse(
            name=updated_order.customer.name,
            phone=updated_order.customer.phone,
            address=updated_order.customer.address
        ),
        items=response_items,
        status=updated_order.status,
        items_total=updated_order.items_total,
        total_items_count=updated_order.total_items_count
    )
