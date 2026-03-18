from fastapi import APIRouter, HTTPException
from app.schemas.order import OrderCreate, OrderRead, OrderUpdate, OrderStatus

router = APIRouter(prefix="/orders", tags=["Orders"])

orders_list = []

@router.post("/", response_model=OrderRead)
def create_order(order: OrderCreate):
    new_order = {
        "order_id" : len(orders_list)+1,
        "user_id" : order.user_id,
        "restaurant_id" : order.restaurant_id,
        "item" : order.item,
        "status" : OrderStatus.Pending,
        "delivery_address": order.delivery_address,
        "contact_number": order.contact_number,
        "tip_amount": order.tip_amount
    }
    orders_list.append(new_order)
    return new_order

@router.get("/", response_model=list[OrderRead])
def get_orders():
    if not orders_list:
        raise HTTPException(status_code=404, detail="Order List Is Empty")
    return orders_list

@router.get("/{order_id}", response_model=OrderRead)
def get_order_by_id(order_id: int):
    for ord in orders_list:
        if ord["order_id"] == order_id:
            return ord
    
    raise HTTPException(status_code=404, detail="Order not found")

@router.put("/{order_id}", response_model=OrderRead)
def update_order(order_id: int, update: OrderUpdate):
    for ord in orders_list:
        if ord["order_id"] == order_id:
            # Guard checks
            if ord["status"] == OrderStatus.Cancelled:
                raise HTTPException(status_code=400, detail="Cannot update a cancelled order")
            if ord["status"] == OrderStatus.Completed:
                raise HTTPException(status_code=400, detail="Cannot update a completed order")

            # Allowed updates (only if Pending or Accepted)
            if update.delivery_address:
                ord["delivery_address"] = update.delivery_address
            if update.contact_number:
                ord["contact_number"] = update.contact_number
            if update.tip_amount is not None:
                ord["tip_amount"] = update.tip_amount

            return ord
    
    raise HTTPException(status_code=404, detail="Order not found")

@router.put("/{order_id}/accept", response_model=OrderRead)
def accept_order(order_id: int):
    for ord in orders_list:
        if ord["order_id"] == order_id:
            if ord["status"] == OrderStatus.Cancelled:
                raise HTTPException(status_code=400, detail="Cannot Accept A Cancelled Order")
            if ord["status"] == OrderStatus.Completed:
                raise HTTPException(status_code=400, detail="Cannot Accept A Completed Order")
            if ord["status"] == OrderStatus.Accepted:
                raise HTTPException(status_code=400, detail="Cannot Accept A Accepted Order")
        
            if ord["status"] == OrderStatus.Pending:
                ord["status"] = OrderStatus.Accepted
                return ord
    
    raise HTTPException(status_code=404, detail="Order Not Found")

@router.put("/{order_id}/complete", response_model=OrderRead)
def complete_order(order_id: int):
    for ord in orders_list:
        if ord["order_id"] == order_id:
            if ord["status"] == OrderStatus.Cancelled:
                raise HTTPException(status_code=400, detail="Cannot Complete A Cancelled Order")
            if ord["status"] == OrderStatus.Pending:
                raise HTTPException(status_code=400, detail="Cannot Complete A Pending Order, Must Be Accepted First")
            if ord["status"] == OrderStatus.Completed:
                raise HTTPException(status_code=400, detail="Order Is Already Completed-")
            
        if ord["status"] == OrderStatus.Accepted:
            ord["status"] = OrderStatus.Completed
            return ord
    
    raise HTTPException(status_code=404, detail="Order Not Found")

@router.put("/{order_id}/cancel", response_model=OrderRead)
def cancel_order(order_id: int):
    for ord in orders_list:
        if ord["order_id"] == order_id:
            if ord["status"] == OrderStatus.Completed:
                raise HTTPException(status_code=400, detail="Cannot cancel a completed order")
            if ord["status"] == OrderStatus.Cancelled:
                raise HTTPException(status_code=400, detail="order already cancelled")
            
            if ord["status"] in [OrderStatus.Pending, OrderStatus.Accepted]:
                ord["status"] = OrderStatus.Cancelled
                return ord
    
    raise HTTPException(status_code=404, detail="Order not found")