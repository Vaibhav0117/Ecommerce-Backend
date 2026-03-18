from fastapi import APIRouter, HTTPException
from app.schemas.user import UserCreate, UserRead

router = APIRouter(prefix="/users", tags=["Users"])

# In-memory storage for now
users = []

@router.post("/", response_model=UserRead)
def create_user(user: UserCreate):
    new_user = {
        "id": len(users) + 1, 
        "name": user.name, 
        "email": user.email
    }
    users.append(new_user)
    return new_user

@router.get("/", response_model=list[UserRead])
def list_users():
    if not users:
        raise HTTPException(status_code=404, detail="User list is empty")
    return users

@router.get("/{user_id}", response_model=UserRead)
def get_user(user_id : int):
    for u in users:
        if u["id"] == user_id:
            return u
            
    raise HTTPException(status_code=404, detail="User not found")
        
@router.put("/{user_id}", response_model=UserRead)
def update_user(user_id: int, updated_user: UserCreate):
    for user in users:
        if user["id"] == user_id:
            user["name"] = updated_user.name
            user["email"] = updated_user.email
            return user
    
    raise HTTPException(status_code=404, detail="User not found")

@router.delete("/{user_id}")
def delete_user(user_id: int):
    for user in users:
        if user["id"] == user_id:
            users.remove(user)
            return {"message": "User Deleted Successfully"}
    
    raise HTTPException(status_code=404, detail="User not found")
