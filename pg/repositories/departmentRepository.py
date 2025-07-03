from sqlalchemy.ext.asyncio import AsyncSession
from pg.repositories.base_repository import BaseRepository
from src.entites.department import Department as DepartmentEntity
from pg.translators.departmentTranslator import DepartmentTranslator
from src.models.departmentModel import DepartmentRead as DepartmentModel

class DepartmentRepository(BaseRepository[DepartmentEntity, DepartmentModel]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, DepartmentEntity, DepartmentTranslator())