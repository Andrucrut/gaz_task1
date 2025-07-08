from pg.translators.base_translator import BaseTranslator
from src.entites.employee import Employee as EmployeeEntity
from src.models.employee_model import EmployeeCreate, Employee as EmployeeModel


class EmployeeTranslator(BaseTranslator[EmployeeEntity, EmployeeModel]):
    entity = EmployeeEntity
    model = EmployeeModel

    def to_entity(self, employee_create: EmployeeCreate) -> EmployeeEntity:
        return EmployeeEntity(
            first_name=employee_create.first_name.strip(),
            last_name=employee_create.last_name.strip(),
            middle_name=employee_create.middle_name.strip(),
            email=employee_create.email.strip().lower(),
            phone_number=employee_create.phone_number,
            birthday=employee_create.birthday,
            position=employee_create.position.strip(),
            salary=employee_create.salary,
            department_id=employee_create.department_id
        )
