from sqlalchemy.ext.asyncio import AsyncSession
from pg.repositories.base_repository import BaseRepository
from src.entites.department import Department
from pg.translators.departmentTranslator import DepartmentTranslator
from src.models.departmentModel import DepartmentRead, DepartmentCreate, DepartmentUpdate


class DepartmentRepository(BaseRepository[Department, DepartmentRead]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Department, DepartmentTranslator())
