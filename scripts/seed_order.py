import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal
from app.models import User, Role, Restaurant, Menu, Order, OrderItem

def seed_order():
    db = SessionLocal()

    # Get the superuser
    user = db.query(User).filter(User.username == "admin").first()
    if not user:
        print("Superuser not found. Run create_superUser.py first.")
        return

    # Get a menu item
    menu_item = db.query(Menu).first()
    if not menu_item:
        print("No menu items found. Run seed_restaurant.py first.")
        return

    # Create an order
    order = Order(
        status="Pending",
        delivery_address="123 Test Street, Hyderabad",
        contact_number="9876543210",
        tip_amount=50,
        user_id=user.user_id, 
        restaurant_id=menu_item.restaurant_id
    )
    db.add(order)
    db.commit()
    db.refresh(order)

    # Create an order item linked to the order and menu item
    order_item = OrderItem(
        order_id=order.order_id, 
        menu_item_id=menu_item.menu_item_id,
        quantity=2
    )
    db.add(order_item)
    db.commit()
    db.refresh(order_item)

    print(f"Order {order.order_id} created for user {user.username} with item {menu_item.name}")

if __name__ == "__main__":
    seed_order()
