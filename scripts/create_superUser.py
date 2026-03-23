from app.database import SessionLocal
from app.models.userModel import User, Role
from app.models.orderModel import Order, OrderItem
from app.models.restaurantModel import Restaurant
from app.models.menuModel import Menu
from app.utils.security import hash_password, verify_password


def create_superuser():
    db = SessionLocal()
    existing_admin = db.query(User).filter(User.role == Role.Admin).first()
    if existing_admin:
        print("Admin already exists.")
        return

    admin = User(
        name="Super Admin",
        username="admin",
        email="admin@example.com",
        password=hash_password("securepassword"),  # replace with your hashing function
        role=Role.Admin
    )
    db.add(admin)
    db.commit()
    db.refresh(admin)
    print(f"Superuser created: {admin.username} ({admin.email})")

if __name__ == "__main__":
    create_superuser()
