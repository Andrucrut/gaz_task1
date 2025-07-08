from pydantic import BaseModel
from typing import Optional
from datetime import datetime



class DepartmentBase(BaseModel):
    name: str
    code: str
    location: str
    description: Optional[str] = None
    phone_number: str


class DepartmentCreate(DepartmentBase):
    pass


class DepartmentRead(DepartmentBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class DepartmentUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    location: Optional[str] = None
    description: Optional[str] = None
    phone_number: Optional[str] = None
