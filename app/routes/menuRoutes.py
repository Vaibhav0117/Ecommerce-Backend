from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.utils.auth import get_current_user
from app.database import get_db
from app.models.userModel import User, Role
from app.models.menuModel import Menu
from app.schemas.menuSchema import MenuItemCreate, MenuItemRead, MenuItemUpdate

router = APIRouter(prefix="/menu_items", tags=["Menu Items"])

# menu_items = []

@router.post("/", response_model=MenuItemRead)
def create_menu(
    menu: MenuItemCreate, 
    db: Session= Depends(get_db),
    current_user: User= Depends(get_current_user)
):
    if current_user.role != Role.Admin:
        raise HTTPException(status_code=403, detail="Only Admin can create menu items")

    db_menu = Menu(
        name = menu.name,
        price = menu.price,
        restaurant_id = menu.restaurant_id
    )
    db.add(db_menu)
    db.commit()
    db.refresh(db_menu)
    return db_menu

    # for list kind of op
    # new_menu = {
    #     "menu_item_id": len(menu_items)+1,
    #     "name": menu.name,
    #     "price": menu.price,
    #     "restaurant_id": menu.restaurant_id
    # }
    # menu_items.append(new_menu)
    # return new_menu


@router.get("/", response_model=list[MenuItemRead])
def get_menu_items(db: Session= Depends(get_db)):
    menu_items = db.query(Menu).all()
    return menu_items

@router.get("/{menu_item_id}", response_model=MenuItemRead)
def get_menu_item(menu_item_id: int, db: Session= Depends(get_db)):
    menu_item = db.query(Menu).filter(Menu.menu_item_id == menu_item_id).first()
    if not menu_item:
        raise HTTPException(status_code=404, detail="Menu Item Not Found")
    return menu_item

    # for men in menu_items:
    #     if men["menu_item_id"] == menu_item_id:
    #         return men
        
    # raise HTTPException(status_code=404, detail="Menu Item Not Found")

@router.put("/{menu_item_id}", response_model=MenuItemRead)
def update_menu(
    menu_item_id: int, 
    updated_menu : MenuItemUpdate, db: Session= Depends(get_db),
    current_user: User= Depends(get_current_user)
):
    if current_user.role != Role.Admin:
        raise HTTPException(status_code=403, detail="Only Admin can update menu items")

    menu_item = db.query(Menu).filter(Menu.menu_item_id == menu_item_id).first()

    if not menu_item:
        raise HTTPException(status_code=404, detail="Menu Item Not Found")
    
    if updated_menu.name is not None:
        menu_item.name = updated_menu.name
    if updated_menu.price is not None:
        menu_item.price = updated_menu.price

    db.commit()
    db.refresh(menu_item)
    return menu_item

    # for men in menu_items:
    #     if men["menu_item_id"] == menu_item_id:
    #         men["name"] = updated_menu.name
    #         men["price"] = updated_menu.price
    #         return men
    
    # raise HTTPException(status_code=404, detail="Menu Item Not Found")

@router.delete("/{menu_item_id}")
def del_menu_item(
    menu_item_id: int, 
    db: Session= Depends(get_db),
    current_user: User= Depends(get_current_user)
):
    if current_user.role != Role.Admin:
        raise HTTPException(status_code=403, detail="Only Admin can delete menu items")
    
    menu_item = db.query(Menu).filter(Menu.menu_item_id == menu_item_id).first()

    if not menu_item:
        raise HTTPException(status_code=404, detail="Menu Item Not Found")
    
    db.delete(menu_item)
    db.commit()
    return {
        "message" : "Menu Item Is Deleted Successfully"
    }

    # for men in menu_items:
    #     if men["menu_item_id"] == menu_item_id:
    #         menu_items.remove(men)
    #         return {
    #             "message": "menu item successfully deleted"
    #         }
        
    # raise HTTPException(status_code=404, detail="Menu Item Not Found")