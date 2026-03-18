from pydantic import BaseModel

class RestaurantCreate(BaseModel):
    name: str
    location: str
    cuisine: str

class RestaurantRead(BaseModel):
    id: int
    name: str
    location: str
    cuisine: str