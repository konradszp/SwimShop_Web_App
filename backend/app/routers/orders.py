from fastapi import APIRouter, HTTPException
from typing import List
from pydantic import BaseModel
from datetime import datetime

from app.repositories.order import OrderRepository
from app.models.order import Order, OrderItem, OrderStatus

from fastapi import Depends
from app.routers.auth import get_current_user
from app.models.user import User

router = APIRouter(
    prefix="/orders",
    tags=["orders"]
)

order_repository = OrderRepository()

class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int
    unit_price: float

class OrderCreate(BaseModel):
    customer_id: int
    user_id: int
    items: List[OrderItemCreate]
    status: OrderStatus = OrderStatus.PENDING

class OrderStatusUpdate(BaseModel):
    status: OrderStatus


class OrderItemResponse(BaseModel):
    order_item_id: int | None = None
    product_id: int
    quantity: int
    unit_price: float

    class Config:
        from_attributes = True

class OrderResponse(BaseModel):
    order_id: int
    customer_id: int
    customer_name: str | None = None
    user_id: int
    order_datetime: datetime
    total_amount: float
    status: OrderStatus
    items: List[OrderItemResponse] = []

    class Config:
        from_attributes = True


@router.get("/", response_model=List[OrderResponse])
def get_all_orders():
    return order_repository.get_all()

@router.get("/{order_id}", response_model=OrderResponse)
def get_order(order_id: int):
    order = order_repository.get_by_id(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    return order

@router.post("/", response_model=OrderResponse, status_code=201)
def create_order(order_data: OrderCreate, current_user: User = Depends(get_current_user)):
    if not order_data.items:
        raise HTTPException(status_code=400, detail="Order must contain at least one item")

    total_amount = sum(item.quantity * item.unit_price for item in order_data.items)

    order = Order(
        customer_id=order_data.customer_id,
        customer_name=None,
        user_id=order_data.user_id,
        order_datetime=datetime.now(),
        total_amount=total_amount,
        status=order_data.status,
        items=[
            OrderItem(
                product_id=item.product_id,
                quantity=item.quantity,
                unit_price=item.unit_price,
            )
            for item in order_data.items
        ],
    )

    order_id = order_repository.create_order(order)
    if not order_id:
        raise HTTPException(status_code=400, detail="Could not create order")

    created = order_repository.get_by_id(order_id)
    if not created:
        raise HTTPException(status_code=500, detail="Order created but could not be retrieved")

    return created

@router.patch("/{order_id}/status", response_model=OrderResponse)
def update_order_status(order_id: int, status_update: OrderStatusUpdate, current_user: User = Depends(get_current_user)):
    existing_order = order_repository.get_by_id(order_id)
    if not existing_order:
        raise HTTPException(status_code=404, detail="Order not found")

    success = order_repository.update_status(order_id, status_update.status)
    if not success:
        raise HTTPException(status_code=400, detail="Could not update order status")

    return order_repository.get_by_id(order_id)