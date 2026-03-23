from pydantic import BaseModel

class RestaurantCreate(BaseModel):
    name: str
    location: str
    cuisine: str

class RestaurantRead(BaseModel):
    restaurant_id: int
    name: str
    location: str
    cuisine: str

    class Config:
        orm_mode = True