from fastapi import APIRouter, HTTPException
from app.schemas.restaurant import RestaurantCreate, RestaurantRead

router = APIRouter(prefix="/restaurants", tags=["Restaurants"])

restaurants = []

@router.post("/", response_model=RestaurantRead)
def create_restaurant(restaurant: RestaurantCreate):
    new_restaurant = {
        "id": len(restaurants)+1,
        "name": restaurant.name,
        "location": restaurant.location,
        "cuisine": restaurant.cuisine,
    }
    restaurants.append(new_restaurant)
    return new_restaurant

@router.get("/", response_model=list[RestaurantRead])
def get_restaurants():
    if not restaurants:
        raise HTTPException(status_code=404, detail="Restaurant list is empty")
    return restaurants

@router.get("/{restaurant_id}", response_model=RestaurantRead)
def get_restaurant_by_id(restaurant_id: int):
    for res in restaurants:
        if res["id"] == restaurant_id:
            return res
    
    raise HTTPException(status_code=404, detail="Restaurant list is empty")

@router.put("/{restaurant_id}", response_model=RestaurantRead)
def update_restaurant(restaurant_id: int, updated_restaurant: RestaurantCreate):
    for restaurant in restaurants:
        if restaurant["id"] == restaurant_id:
            restaurant["name"] = updated_restaurant.name
            restaurant["location"] = updated_restaurant.location
            restaurant["cuisine"] = updated_restaurant.cuisine
            return restaurant
    
    raise HTTPException(status_code=404, detail="Restaurant Not Found")

@router.delete("/{restaurant_id}")
def delete_restaurant(restaurant_id: int):
    for res in restaurants:
        if res["id"] == restaurant_id:
            restaurants.remove(res)
            return {"message": "Restaurant Is Deleted Successfully"}
    
    raise HTTPException(status_code=404, detail="Restaurant Not Found")

