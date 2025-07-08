from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pg.connection import get_async_session
from pg.repositories.employee_repository import EmployeeRepository
from pg.repositories.department_repository import DepartmentRepository
from pg.repositories.project_repository import ProjectRepository


class DBManager:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.employee_repo = EmployeeRepository(session)
        self.department_repo = DepartmentRepository(session)
        self.project_repo = ProjectRepository(session)
