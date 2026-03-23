from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class Restaurant(Base):
    __tablename__ = "restaurants"

    restaurant_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    cuisine = Column(String, nullable=False)

    # A restaurant can offer multiple menu items.
    menus = relationship("Menu", back_populates="restaurant")

    # A restaurant can receive multiple orders.
    orders = relationship("Order", back_populates="restaurant")