from pg.repositories.employeeRepository import EmployeeRepository
from pg.repositories.departmentRepository import DepartmentRepository

class DBManager:
    def __init__(self, session):
        self.session = session
        self.employee_repo = EmployeeRepository(session)
        self.department_repo = DepartmentRepository(session)