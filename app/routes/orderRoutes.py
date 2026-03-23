from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.utils.auth import get_current_user
from app.database import get_db
from app.models.userModel import User, Role
from app.models.orderModel import Order
from app.schemas.orderSchema import OrderCreate, OrderRead, OrderUpdate, OrderStatus

router = APIRouter(prefix="/orders", tags=["Orders"])

# orders_list = []

@router.post("/", response_model=OrderRead)
def create_order(
    order: OrderCreate, 
    db: Session = Depends(get_db),
    current_user: User= Depends(get_current_user)
):
    if current_user.role != Role.Customer:
        raise HTTPException(status_code=403, detail="Only Customers can place orders")
    
    db_order = Order(
        customer_id=current_user.user_id,
        status = OrderStatus.Pending,
        delivery_address = order.delivery_address,
        contact_number = order.contact_number,
        tip_amount = order.tip_amount
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

@router.get("/", response_model=list[OrderRead])
def get_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role == Role.Customer:
        orders = db.query(Order).filter(Order.customer_id == current_user.user_id).all()
    else:  # Admin
        orders = db.query(Order).all()

    if not orders:
        raise HTTPException(status_code=404, detail="Order List Is Empty")
    return orders

@router.get("/{order_id}", response_model=OrderRead)
def get_order(
    order_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    order = db.query(Order).filter(Order.order_id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order Not Found")
    
    if current_user.role == Role.Customer and order.customer_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="Not authorized to view this order")
    
    return order

@router.put("/{order_id}", response_model=OrderRead)
def update_order(
    order_id: int, 
    updated_order: OrderUpdate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    order = db.query(Order).filter(Order.order_id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order Not Found")
    
    if current_user.role == Role.Customer and order.customer_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="Not authorized to update this order")
    
    if order.status in [OrderStatus.Cancelled, OrderStatus.Completed]:
        raise HTTPException(status_code=400, detail=f"Cannot update order in {order.status} state")
    
    order.delivery_address = updated_order.delivery_address
    order.contact_number = updated_order.contact_number
    order.tip_amount = updated_order.tip_amount
    order.status = updated_order.status
    db.commit()
    db.refresh(order)
    return order


@router.put("/{order_id}/accept", response_model=OrderRead)
def accept_order(
    order_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != Role.Admin:
        raise HTTPException(status_code=403, detail="Only Admin can accept orders")
    
    order = db.query(Order).filter(Order.order_id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order Not Found")
    
    if order.status in [OrderStatus.Cancelled, OrderStatus.Completed, OrderStatus.Accepted]:
        raise HTTPException(status_code=400, detail=f"Cannot accept order in {order.status} state")
    
    order.status = OrderStatus.Accepted
    db.commit()
    db.refresh(order)
    return order
    
    # for ord in orders_list:
    #     if ord["order_id"] == order_id:
    #         if ord["status"] in [OrderStatus.Cancelled, OrderStatus.Completed, OrderStatus.Accepted]:
    #             raise HTTPException(status_code=400, detail=f"Cannot Accept Order In {ord['status']} State")
    #         if ord["status"] == OrderStatus.Pending:
    #             ord["status"] = OrderStatus.Accepted
    #             return ord
    # raise HTTPException(status_code=404, detail="Order Not Found")

@router.put("/{order_id}/complete", response_model=OrderRead)
def complete_order(
    order_id: int, 
    db: Session = Depends(get_db),
    current_user: User=  Depends(get_current_user)
):
    if current_user.role != Role.Admin:
        raise HTTPException(status_code=403, detail="Only Admin can complete orders")
    
    order = db.query(Order).filter(Order.order_id == order_id).first()

    if not order:
        raise HTTPException(status_code=404, detail="Order Not Found")
    
    if order.status in [OrderStatus.Pending, OrderStatus.Cancelled, OrderStatus.Completed]:
        raise HTTPException(status_code=400, detail=f"Cannot Complete order in {order.status} state")
    
    order.status = OrderStatus.Completed
    db.commit()
    db.refresh(order)
    return order

    # for ord in orders_list:
    #     if ord["order_id"] == order_id:
    #         if ord["status"] == OrderStatus.Cancelled:
    #             raise HTTPException(status_code=400, detail="Cannot Complete a Cancelled Order")
    #         if ord["status"] == OrderStatus.Pending:
    #             raise HTTPException(status_code=400, detail="Cannot Complete A Pending Order, Must Be Accepted First")
    #         if ord["status"] == OrderStatus.Completed:
    #             raise HTTPException(status_code=400, detail="Order is Already Completed")
    #         if ord["status"] == OrderStatus.Accepted:
    #             ord["status"] = OrderStatus.Completed
    #             return ord
            
    # raise HTTPException(status_code=404, detail="Order Not Found")

@router.put("/{order_id}/cancel", response_model=OrderRead)
def cancel_order(
    order_id: int, 
    db: Session = Depends(get_db),
    current_user: User= Depends(get_current_user)
):
    order = db.query(Order).filter(Order.order_id == order_id).first()

    if not order:
        raise HTTPException(status_code=404, detail="Order Not Found")
    
    if current_user.role == Role.Customer and order.customer_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="Not authorized to cancel this order")
    
    if order.status == OrderStatus.Completed:
        raise HTTPException(status_code=400, detail="Cannot Cancel A Complete Order")
    if order.status == OrderStatus.Cancelled:
        raise HTTPException(status_code=400, detail="Order Is Cancelled")

    order.status = OrderStatus.Cancelled
    db.commit()
    db.refresh(order)
    return order    
    # for ord in orders_list:
    #     if ord["order_id"] == order_id:
    #         if ord["status"] == OrderStatus.Completed:
    #             raise HTTPException(status_code=400, detail="Cannot Cancel A Completed Order")
    #         if ord["status"] == OrderStatus.Cancelled:
    #             raise HTTPException(status_code=400, detail="Order Already Cancelled")
            
    #         if ord["status"] in [OrderStatus.Pending, OrderStatus.Accepted]:
    #             ord["status"] = OrderStatus.Cancelled
    #             return ord
    
    # raise HTTPException(status_code=404, detail="Order Not Found")