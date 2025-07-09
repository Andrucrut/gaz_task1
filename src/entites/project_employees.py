from sqlalchemy import Table, Column, Integer, ForeignKey
from pg.settings import Base

project_employees = Table(
    'project_employees',
    Base.metadata,
    Column('project_id', Integer, ForeignKey('projects.id'), primary_key=True),
    Column('employee_id', Integer, ForeignKey('employees.id'), primary_key=True)
)
