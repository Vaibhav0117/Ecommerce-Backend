import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal
from app.models import User, Role, Restaurant, Menu, Order, OrderItem

def seed_restaurant():
    db = SessionLocal()

    # Create a restaurant
    restaurant = Restaurant(
        name="Testaurant",
        location="Hyderabad",
        cuisine="Indian"
    )
    db.add(restaurant)
    db.commit()
    db.refresh(restaurant)

    # Create a menu item linked to the restaurant
    menu_item = Menu(
        name="Paneer Butter Masala",
        price=250,
        restaurant_id=restaurant.restaurant_id
    )
    db.add(menu_item)
    db.commit()
    db.refresh(menu_item)

    print(f"Restaurant: {restaurant.name}, Menu Item: {menu_item.name}")

if __name__ == "__main__":
    seed_restaurant()
