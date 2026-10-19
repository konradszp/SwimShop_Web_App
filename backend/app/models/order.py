from datetime import datetime
from enum import Enum
from typing import List
from pydantic import BaseModel, Field

class OrderStatus(str, Enum):
    COMPLETED = 'completed'
    CANCELLED = 'cancelled'
    PENDING = 'pending'

class OrderItem(BaseModel):
    product_id: int
    quantity: int
    unit_price: float
    order_item_id: int | None = None
    order_id: int | None = None

    @property
    def subtotal(self) -> float:
        return self.quantity * self.unit_price

class Order(BaseModel):
    customer_id: int
    user_id: int
    order_datetime: datetime
    total_amount: float
    status: OrderStatus
    order_id: int | None = None
    customer_name: str | None = None
    items: List[OrderItem]= Field(default_factory=list)
    