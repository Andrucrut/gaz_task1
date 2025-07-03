from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from decimal import Decimal


class EmployeeBase(BaseModel):
    first_name: str
    last_name: str
    middle_name: str
    email: EmailStr
    phone_number: Optional[str] = None
    birthday: datetime
    position: str
    salary: Decimal
    department_id: int


class EmployeeCreate(EmployeeBase):
    pass


class Employee(EmployeeBase):
    id: int

    class Config:
        orm_mode = True


class EmployeeUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    middle_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    birthday: Optional[datetime] = None
    position: Optional[str] = None
    salary: Optional[Decimal] = None
    department_id: Optional[int] = None
