from pydantic import BaseModel
from enum import Enum

class OrderStatus(str, Enum):
    Pending = "Pending"
    Accepted = "Accepted"
    Completed = "Completed"
    Cancelled = "Cancelled"

class OrderItemCreate(BaseModel):
    menu_item_id: int
    quantity: int

class OrderItemRead(BaseModel):
    id: int
    menu_item_id: int
    quantity: int

    class Config:
        orm_mode = True

class OrderCreate(BaseModel):
    user_id: int
    restaurant_id: int
    items: list[OrderItemCreate]
    delivery_address: str
    contact_number: str
    tip_amount: float | None = None

class OrderRead(BaseModel):
    order_id : int
    user_id : int
    restaurant_id : int
    items: list[OrderItemRead]
    status: OrderStatus
    delivery_address : str
    contact_number : str
    tip_amount: float | None = None

    class config:
        orm_mode = True

class OrderUpdate(BaseModel):
    delivery_address: str | None = None
    contact_number: str | None = None
    tip_amount: float | None = None
    status: OrderStatus | None = None