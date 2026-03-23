from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship
from app.database import Base
import enum

class Role(enum.Enum):
    Customer = "Customer"
    Admin = "Admin"

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    username = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(Enum(Role), default=Role.Customer)

    # A user can place multiple orders.
    orders = relationship("Order", back_populates="user")
