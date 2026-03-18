from fastapi import APIRouter, HTTPException
from app.schemas.menu import MenuItemCreate, MenuItemRead

router = APIRouter(prefix="/menu_items", tags=["Menu_Items"])

menu_items = []

@router.post("/", response_model=MenuItemRead)
def create_menu(menu: MenuItemCreate):
    new_menu = {
        "id": len(menu_items)+1,
        "name": menu.name,
        "price": menu.price,
        "restaurant_id": menu.restaurant_id
    }
    menu_items.append(new_menu)
    return new_menu

@router.get("/", response_model=list[MenuItemRead])
def get_menu():
    if not menu_items:
        raise HTTPException(status_code=404, detail="Menu List Is Empty")
    return menu_items

@router.get("/{menu_id}", response_model=MenuItemRead)
def get_menu_by_id(menu_id: int):
    for men in menu_items:
        if men["id"] == menu_id:
            return men
        
    raise HTTPException(status_code=404, detail="Menu Item Not Found")

@router.put("/{menu_id}", response_model=MenuItemRead)
def update_menu(menu_id: int, updated_menu : MenuItemCreate):
    for men in menu_items:
        if men["id"] == menu_id:
            men["name"] = updated_menu.name
            men["price"] = updated_menu.price
            men["restaurant_id"] = updated_menu.restaurant_id
            return men
    
    raise HTTPException(status_code=404, detail="Menu Item Not Found")

@router.delete("/{menu_id}")
def del_menu_item(menu_id: int):
    for men in menu_items:
        if men["id"] == menu_id:
            menu_items.remove(men)
            return {
                "message": "menu item successfully deleted"
            }
        
    raise HTTPException(status_code=404, detail="Menu Item Not Found")