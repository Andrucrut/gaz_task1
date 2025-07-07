from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from pg.connection import Base
from .project_employees import project_employees


class Project(Base):
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=True)
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    employees = relationship(
        "Employee",
        secondary=project_employees,
        back_populates="projects"
    )
