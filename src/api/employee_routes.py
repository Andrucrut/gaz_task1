from fastapi import APIRouter, Depends
from typing import List

from src.models.employeeModel import EmployeeCreate, EmployeeRead
from pg.manager import DBManager, get_db_manager

router = APIRouter(prefix="/employees", tags=["employees"])

@router.post("/", response_model=EmployeeRead)
async def create_employee(
    employee: EmployeeCreate,
    db_manager: DBManager = Depends(get_db_manager)
):
    return await db_manager.employee_repo.add_model(employee)


@router.get("/by_department/{department_id}", response_model=List[EmployeeRead])
async def get_employees_by_department(
    department_id: int,
    db_manager: DBManager = Depends(get_db_manager)
):
    return await db_manager.employee_repo.get_employees_by_department(department_id)


@router.get("/", response_model=List[EmployeeRead])
async def get_employees(
    db_manager: DBManager = Depends(get_db_manager)
):
    return await db_manager.employee_repo.get_all()
