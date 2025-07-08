from fastapi import APIRouter, Depends
from typing import List
from pg.dependencies import get_db_manager

from src.models.employee_model import EmployeeCreate, EmployeeRead
from pg.manager import DBManager

router = APIRouter(prefix="/employees", tags=["employees"])


@router.post("/", response_model=EmployeeRead)
async def create_employee(
    employee: EmployeeCreate,
    db_manager: DBManager = Depends(get_db_manager)
):
    async for repo in db_manager.get_employee_repo():
        return await repo.add_model(employee)


@router.get("/by_department/{department_id}", response_model=List[EmployeeRead])
async def get_employees_by_department(
    department_id: int,
    db_manager: DBManager = Depends(get_db_manager)
):
    async for repo in db_manager.get_employee_repo():
        return await repo.get_employees_by_department(department_id)


@router.get("/", response_model=List[EmployeeRead])
async def get_employees(
    db_manager: DBManager = Depends(get_db_manager)
):
    async for repo in db_manager.get_employee_repo():
        return await repo.get_all()