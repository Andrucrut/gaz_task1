from pg.translators.base_translator import BaseTranslator
from src.models.departmentModel import DepartmentCreate, DepartmentRead as DepartmentModel
from src.entites.department import Department as DepartmentEntity

class DepartmentTranslator(BaseTranslator[DepartmentEntity, DepartmentModel]):
    entity = DepartmentEntity
    model = DepartmentModel

    def to_entity(self, department_create: DepartmentCreate) -> DepartmentEntity:
        return DepartmentEntity(
            name=department_create.name.strip(),
            code=department_create.code.strip().upper(),
            location=department_create.location.strip(),
            description=department_create.description,
            phone_number=department_create.phone_number
        )

