from fastapi import FastAPI
from app.routes import users, restaurants, menu, orders, admin

app = FastAPI()

# Include routers
app.include_router(users.router)
app.include_router(restaurants.router)
app.include_router(menu.router)
app.include_router(orders.router)
app.include_router(admin.router)

@app.get("/")
def root():
    return {"message": "Backend API is running"}
