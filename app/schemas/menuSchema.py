from pydantic import BaseModel

class MenuItemBase(BaseModel):
    name: str
    price: int   

class MenuItemCreate(MenuItemBase):
    restaurant_id : int

class MenuItemRead(BaseModel):
    menu_item_id : int
    name : str
    price : int
    restaurant_id : int

    class Config:
        orm_mode = True

class MenuItemUpdate(BaseModel):
    name: str | None = None
    price: int | None = None
