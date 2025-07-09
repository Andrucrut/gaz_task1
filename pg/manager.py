from pg.repositories.employee_repository import EmployeeRepository
from pg.repositories.department_repository import DepartmentRepository
from pg.repositories.project_repository import ProjectRepository


class DBManager:
    def get_employee_repo(self, session):
        return EmployeeRepository(session)

    def get_department_repo(self, session):
        return DepartmentRepository(session)

    def get_project_repo(self, session):
        return ProjectRepository(session)
