from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.utils.auth import get_current_user
from app.database import get_db
from app.models.userModel import User, Role
from app.schemas.adminSchema import AdminCreate, AdminRead, AdminUpdate

router = APIRouter(prefix="/admins", tags=["Admins"])

admin_list = []

@router.post("/", response_model=AdminRead)
def create_Admin(
    admin: AdminCreate, 
    db: Session = Depends(get_db),
    current_user: User= Depends(get_current_user)
):
    db_admin = User(
        name = admin.name,
        username = admin.username,
        email = admin.email,
        password = admin.password,
        role = Role.Admin
    )
    db.add(db_admin)
    db.commit()
    db.refresh(db_admin)
    return db_admin

    # new_admin = {
    #     "user_id": len(admin_list)+1,
    #     "name": admin.name,
    #     "email": admin.email,
    #     "password": admin.password,
    #     "role": admin.role
    # }
    # admin_list.append(new_admin)
    # return new_admin

@router.get("/", response_model=list[AdminRead])
def get_admins(db: Session= Depends(get_db)):
    users = db.query(User).filter(User.role == Role.admin).all()
    return users

@router.get("/{admin_id}", response_model=AdminRead)
def get_admin_by_id(admin_id: int, db: Session= Depends(get_db)):
    user = db.query(User).filter(User.user_id == admin_id, User.role == Role.admin).first()
    if not user:
        raise HTTPException(status_code=404, detail="Admin Not Found")
    return user

    # for ad in admin_list:
    #     if ad["user_id"] == admin_id:
    #         return ad
    
    # raise HTTPException(status_code=404, detail="Admin Not Found")

@router.put("/{admin_id}", response_model=AdminRead)
def update_ad_profile(admin_id: int, admin_update: AdminUpdate, db: Session= Depends(get_db)):
    admin = db.query(User).filter(User.user_id == admin_id, User.role == Role.Admin).first()

    if admin_update.name is not None:
        admin.name = admin_update.name
    if admin_update.username is not None:
        admin.username = admin_update.username
    if admin_update.email is not None:
        admin.email = admin_update.email
    if admin_update.password is not None:
        admin.password = admin_update.password
    
    db.commit()
    db.refresh(admin)
    return admin

    # for ad in admin_list:
    #     if ad["user_id"] == admin_id:
    #         if admin_update.name is not None:
    #             ad["name"] = admin_update.name
    #         if admin_update.email is not None:
    #             ad["email"] = admin_update.email
    #         if admin_update.password is not None:
    #             ad["password"] = admin_update.password
    #         if admin_update.role is not None:
    #             ad["role"] = admin_update.role
    #         return ad
    
    # raise HTTPException(status_code=404, detail="Admin Not Found")

@router.delete("/{admin_id}")
def del_admin(admin_id: int, db: Session= Depends(get_db)):
    admin = db.query(User).filter(User.user_id == admin_id, User.role == Role.Admin).first()
    if not admin:
        raise HTTPException(status_code=404, detail="Admin Not Found")

    db.delete(admin)
    db.commit()

    return {"message": "Admin Deleted Successfully"}
    # for adm in admin_list:
    #     if adm["user_id"] == admin_id:
    #         admin_list.remove(adm)
    #         return {
    #             "message": "Admin Deleted Successfully"
    #         }
    
    # raise HTTPException(status_code=404, detail="Admin Not Found")