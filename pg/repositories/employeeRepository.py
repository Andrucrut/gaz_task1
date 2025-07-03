from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.entites.employee import Employee
from typing import Sequence
from pg.repositories.base_repository import BaseRepository
from pg.translators.employeeTranslator import EmployeeTranslator
from src.models.employeeModel import EmployeeRead

class EmployeeRepository(BaseRepository[Employee, EmployeeRead]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Employee, EmployeeTranslator())

    async def get_employees_by_department(self, department_id: int) -> Sequence[EmployeeRead]:
        result = await self.session.execute(
            select(self.model).where(self.model.department_id == department_id)
        )
        orm_objs = result.scalars().all()
        return self.translator.to_model_many(orm_objs)