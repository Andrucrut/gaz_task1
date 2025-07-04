from pg.repositories.employeeRepository import EmployeeRepository
from pg.repositories.departmentRepository import DepartmentRepository
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from pg.connection import get_async_session

class DBManager:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.employee_repo = EmployeeRepository(session)
        self.department_repo = DepartmentRepository(session)

    @classmethod
    async def __call__(cls, session: AsyncSession = Depends(get_async_session)):
        return cls(session)
