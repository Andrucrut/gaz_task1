from pg.translators.base_translator import BaseTranslator
from src.models.departmentModel import DepartmentCreate, DepartmentRead
from src.entites.department import Department


class DepartmentTranslator(BaseTranslator[Department, DepartmentRead]):
    entity = Department
    model = DepartmentRead

    def to_entity(self, department_create: DepartmentCreate) -> Department:
        return Department(
            name=department_create.name.strip(),
            code=department_create.code.strip().upper(),
            location=department_create.location.strip(),
            description=department_create.description,
            phone_number=department_create.phone_number
        )