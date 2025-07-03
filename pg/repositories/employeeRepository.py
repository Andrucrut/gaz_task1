from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.entites.employee import Employee as EmployeeEntity
from typing import Sequence
from pg.repositories.base_repository import BaseRepository
from pg.translators.employeeTranslator import EmployeeTranslator
from src.models.employeeModel import Employee as EmployeeModel

class EmployeeRepository(BaseRepository[EmployeeEntity, EmployeeModel]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, EmployeeEntity, EmployeeTranslator())

    async def get_employees_by_department(self, department_id: int) -> Sequence[EmployeeModel]:
        result = await self.session.execute(
            select(self.entity).where(self.entity.department_id == department_id)
        )
        entity_objs = list(result.scalars().all())
        return self.translator.to_model_many(entity_objs)