from pydantic import BaseModel
from typing import Optional

class AdminCreate(BaseModel):
    name: str
    username: str
    email: str
    password: str
    role: str = "admin"      # role comes from User model enum 

class AdminRead(BaseModel):
    user_id: int             # align with User model PK
    name: str
    username: str
    email: str
    role: str

    class Config:
        orm_mode = True

class AdminUpdate(BaseModel):
    name: Optional[str] = None
    username: str | None = None
    email: Optional[str] = None
    password: Optional[str] = None
    role: Optional[str] = None

