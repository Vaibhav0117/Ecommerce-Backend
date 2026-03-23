from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.database import Base
import enum

class OrderStatus(enum.Enum):
    Pending = "Pending"
    Accepted = "Accepted"
    Completed = "Completed"
    Cancelled = "Cancelled"

class Order(Base):
    __tablename__ = "orders"

    order_id = Column(Integer, primary_key=True, index=True)
    status = Column(Enum(OrderStatus), default=OrderStatus.Pending)
    delivery_address = Column(String, nullable=False)
    contact_number = Column(String, nullable=False)
    tip_amount = Column(Float, nullable=True)

    # Foreign Keys
    user_id = Column(Integer, ForeignKey("users.user_id"))
    restaurant_id = Column(Integer, ForeignKey("restaurants.restaurant_id"))

    # Relationships
    # One user can place many orders
    user = relationship("User", back_populates="orders")
    # One restaurant can receive many orders
    restaurant = relationship("Restaurant", back_populates="orders")
    # One order can contain multiple items
    items = relationship("OrderItem", back_populates="order")

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.order_id"))
    menu_item_id = Column(Integer, ForeignKey("menu_items.menu_item_id"))
    quantity = Column(Integer, nullable=False)

    # Relationships
    # Each order item belongs to one order
    order = relationship("Order", back_populates="items")
    # Each order item refers to one menu item
    menu = relationship("Menu", back_populates="order_items")

