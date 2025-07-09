from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from pg.settings import Base


class Department(Base):
    __tablename__ = 'departments'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    code = Column(String, nullable=False, unique=True)
    location = Column(String, nullable=False)
    description = Column(String, nullable=True)
    phone_number = Column(String, nullable=True, unique=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    employees = relationship("Employee", back_populates="department")