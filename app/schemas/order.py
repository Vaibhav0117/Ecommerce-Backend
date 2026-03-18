from pydantic import BaseModel
from enum import Enum

class OrderStatus(str, Enum):
    Pending = "Pending"
    Accepted = "Accepted"
    Completed = "Completed"
    Cancelled = "Cancelled"

class OrderCreate(BaseModel):
    user_id: int
    restaurant_id : int
    item : list[int]
    delivery_address : str
    contact_number : str
    tip_amount: float | None = None

class OrderRead(BaseModel):
    order_id : int
    user_id : int
    restaurant_id : int
    item : list[int]
    status: OrderStatus
    delivery_address : str
    contact_number : str
    tip_amount: float | None = None

class OrderUpdate(BaseModel):
    delivery_address: str | None = None
    contact_number: str | None = None
    tip_amount: float | None = None 