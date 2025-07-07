from sqlalchemy import Column, Integer, String, DateTime, func, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from pg.connection import Base
from .project_employees import project_employees


class Employee(Base):
    __tablename__ = 'employees'

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    middle_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    birthday = Column(DateTime, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    phone_number = Column(String, nullable=False)
    position = Column(String, nullable=False)
    salary = Column(Numeric(9, 2), nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"))

    department = relationship("Department", back_populates="employees")
    projects = relationship(
        "Project",
        secondary=project_employees,
        back_populates="employees"
    )
