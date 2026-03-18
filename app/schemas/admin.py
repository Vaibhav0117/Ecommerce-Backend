from pydantic import BaseModel
from typing import Optional

class AdminCreate(BaseModel):
    name: str
    email: str
    password: str
    role: str = "admin"

class AdminRead(BaseModel):
    id: int
    name: str
    email: str
    role: str

class AdminUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    role: Optional[str] = None

