from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pg.connection import get_async_session
from pg.repositories.employeeRepository import EmployeeRepository
from pg.repositories.departmentRepository import DepartmentRepository
from pg.repositories.projectRepository import ProjectRepository


class DBManager:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.employee_repo = EmployeeRepository(session)
        self.department_repo = DepartmentRepository(session)
        self.project_repo = ProjectRepository(session)

async def get_db_manager(session: AsyncSession = Depends(get_async_session)) -> DBManager:
    return DBManager(session)
