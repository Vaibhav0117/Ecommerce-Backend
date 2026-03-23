from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.userModel import User

def get_current_user(user_id: int, db: Session = Depends(get_db)) -> User:
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid user")
    return user
