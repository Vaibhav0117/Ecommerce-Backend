from pydantic import BaseModel

class MenuItemCreate(BaseModel):
    name : str
    price : int
    restaurant_id : int

class MenuItemRead(BaseModel):
    id : int
    name : str
    price : int
    restaurant_id : int