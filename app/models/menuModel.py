from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Menu(Base):
    __tablename__ = "menu_items"

    menu_item_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    price = Column(Integer, nullable=False)

    restaurant_id = Column(Integer, ForeignKey("restaurants.restaurant_id"), nullable=False)

    # Each menu item belongs to one restaurant.
    restaurant = relationship("Restaurant", back_populates="menus")

    # A menu item can appear in multiple order items.
    order_items = relationship("OrderItem", back_populates="menu")

