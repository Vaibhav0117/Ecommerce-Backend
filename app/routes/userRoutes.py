from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.userModel import User, Role
from app.schemas.userSchema import UserCreate, UserRead

router = APIRouter(prefix="/users", tags=["Users"])

# In-memory storage for now
# users = []

@router.post("/", response_model=UserRead)
# Add a new user to the database
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(
        name = user.name,
        email = user.email,
        password = user.password,
        role = Role.Customer
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/", response_model=list[UserRead])
# Get all users from the database
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    if not users:
        raise HTTPException(status_code=404, detail="User list is empty")
    return users

@router.get("/{user_id}", response_model=UserRead)
# Get a single user by ID
def get_user(user_id : int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User Not Found")
    return user
        
@router.put("/{user_id}", response_model=UserRead)
# Update an existing user by ID
def update_user(user_id: int, updated_user: UserCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.name = updated_user.name
    user.email = updated_user.email
    user.password = updated_user.password
    
    db.commit()
    db.refresh(user)
    return user

@router.delete("/{user_id}")
# Delete a user by ID
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.user_id == user_id, User.role == Role.Customer).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {
        "message": "User Deleted Successfully"
    }