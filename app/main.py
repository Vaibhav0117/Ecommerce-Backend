from fastapi import FastAPI
from app.database import Base, engine

# Import all routers (API endpoints)
from app.routes.userRoutes import router as user_router
from app.routes.restaurantRoutes import router as restaurant_router
from app.routes.orderRoutes import router as order_router
from app.routes.menuRoutes import router as menu_router
from app.routes.adminRoutes import router as admin_router

# Import all models so SQLAlchemy registers them
# Without these imports, Base.metadata.create_all() won't know about the tables
from app.models.userModel import User
from app.models.restaurantModel import Restaurant
from app.models.orderModel import Order
from app.models.menuModel import Menu

# Initialize FastAPI application
app = FastAPI()

# Register routers with the app
app.include_router(user_router)          # User-related routes
app.include_router(restaurant_router)    # Restaurant-related routes
app.include_router(menu_router)           # Menu-related routes
app.include_router(order_router)         # Order-related routes
app.include_router(admin_router)          # Admin-related routes

# Create all tables in the database (if they don't already exist)
# This scans all models that inherit from Base and generates tables
Base.metadata.create_all(bind=engine)

# Root endpoint to verify API is running
@app.get("/")
def root():
    return {
        "message": "Backend API is running"
    }
