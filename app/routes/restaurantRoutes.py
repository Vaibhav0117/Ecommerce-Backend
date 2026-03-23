from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.utils.auth import get_current_user
from app.models.restaurantModel import Restaurant
from app.models.userModel import User, Role
from app.schemas.restaurantSchema import RestaurantCreate, RestaurantRead

router = APIRouter(prefix="/restaurants", tags=["Restaurants"])

# restaurants = []

@router.post("/", response_model=RestaurantRead)
def create_restaurant(
    restaurant: RestaurantCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    if current_user.role != Role.Admin:
        raise HTTPException(status_code=403, detail="Only Admin can create restaurants")

    db_restaurant = Restaurant(
        name = restaurant.name,
        location = restaurant.location,
        cuisine = restaurant.cuisine
    )
    db.add(db_restaurant)
    db.commit()
    db.refresh(db_restaurant)
    return db_restaurant

@router.get("/", response_model=list[RestaurantRead])
def get_restaurants(db: Session = Depends(get_db)):
    restaurants = db.query(Restaurant).all()
    if not restaurants:
        raise HTTPException(status_code=404, detail="Restaurant list is empty")
    return restaurants

@router.get("/{restaurant_id}", response_model=RestaurantRead)
def get_restaurant(restaurant_id: int, db: Session = Depends(get_db)):
    restaurant = db.query(Restaurant).filter(Restaurant.restaurant_id == restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant Not Found")
    return restaurant

@router.put("/{restaurant_id}", response_model=RestaurantRead)
def update_restaurant(
    restaurant_id: int,
    updated_restaurant: RestaurantCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != Role.Admin:
        raise HTTPException(status_code=403, detail="Only Admin can update restaurants")
    
    restaurant = db.query(Restaurant).filter(Restaurant.restaurant_id == restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant Not Found")
    
    restaurant.name = updated_restaurant.name
    restaurant.location = updated_restaurant.location
    restaurant.cuisine = updated_restaurant.cuisine
    db.commit()
    db.refresh(restaurant)
    return restaurant

@router.delete("/{restaurant_id}")
def delete_restaurant(
    restaurant_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != Role.Admin:
        raise HTTPException(status_code=403, detail="Only Admin can update restaurants")
    
    restaurant = db.query(Restaurant).filter(Restaurant.restaurant_id == restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant Not Found")
    db.delete(restaurant)
    db.commit()
    return {
        "message": "Restaurant Deleted Successfully"
    }
    

