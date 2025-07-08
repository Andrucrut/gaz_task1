from sqlalchemy.ext.asyncio import AsyncSession
from pg.repositories.employee_repository import EmployeeRepository
from pg.repositories.department_repository import DepartmentRepository
from pg.repositories.project_repository import ProjectRepository
from pg.connection import AsyncSessionLocal


class DBManager:
    def __init__(self, session_factory=AsyncSessionLocal):
        self.session_factory = session_factory

    async def get_employee_repo(self):
        async with self.session_factory() as session:
            yield EmployeeRepository(session)

    async def get_department_repo(self):
        async with self.session_factory() as session:
            yield DepartmentRepository(session)

    async def get_project_repo(self):
        async with self.session_factory() as session:
            yield ProjectRepository(session)