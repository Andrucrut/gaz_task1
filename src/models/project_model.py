from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class Project(BaseModel):
    name: str
    description: str
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class ProjectCreate(Project):
    pass


class ProjectRead(Project):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None