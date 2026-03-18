from fastapi import APIRouter, HTTPException
from app.schemas.admin import AdminCreate, AdminRead, AdminUpdate

router = APIRouter(prefix="/admin", tags=["Admin"])

admin_list = []

@router.post("/", response_model=AdminRead)
def create_Admin(admin: AdminCreate):
    new_admin = {
        "id": len(admin_list)+1,
        "name": admin.name,
        "email": admin.email,
        "password": admin.password,
        "role": admin.role
    }
    admin_list.append(new_admin)
    return new_admin

@router.get("/", response_model=list[AdminRead])
def get_admins():
    if not admin_list:
        raise HTTPException(status_code= 404, detail="Admin List Is Empty")
    
    return admin_list

@router.get("/{admin_id}", response_model=AdminRead)
def get_admin_by_id(admin_id: int):
    for ad in admin_list:
        if ad["id"] == admin_id:
            return ad
    
    raise HTTPException(status_code=404, detail="Admin Not Found")

@router.put("/{admin_id}", response_model=AdminRead)
def update_ad_profile(admin_id: int, admin_update: AdminUpdate):
    for ad in admin_list:
        if ad["id"] == admin_id:
            if admin_update.name is not None:
                ad["name"] = admin_update.name
            if admin_update.email is not None:
                ad["email"] = admin_update.email
            if admin_update.password is not None:
                ad["password"] = admin_update.password
            if admin_update.role is not None:
                ad["role"] = admin_update.role
            return ad
    
    raise HTTPException(status_code=404, detail="Admin Not Found")

@router.delete("/{admin_id}")
def del_admin(admin_id: int):
    for adm in admin_list:
        if adm["id"] == admin_id:
            admin_list.remove(adm)
            return {"message": "Admin Deleted Successfully"}
    
    raise HTTPException(status_code=404, detail="Admin Not Found")