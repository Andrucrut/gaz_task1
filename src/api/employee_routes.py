from fastapi import APIRouter, Depends
from typing import List
from pg.settings import get_db_manager, get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.employee_model import EmployeeCreate, EmployeeRead
from pg.manager import DBManager

router = APIRouter(prefix="/employees", tags=["employees"])


@router.post("/", response_model=EmployeeRead)
async def create_employee(
        employee: EmployeeCreate,
        db_manager: DBManager = Depends(get_db_manager),
        session: AsyncSession = Depends(get_async_session)
):
    repo = db_manager.get_employee_repo(session)
    return await repo.add_model(employee)


@router.get("/by_department/{department_id}", response_model=List[EmployeeRead])
async def get_employees_by_department(
        department_id: int,
        db_manager: DBManager = Depends(get_db_manager),
        session: AsyncSession = Depends(get_async_session)
):
    repo = db_manager.get_employee_repo(session)
    return await repo.get_employees_by_department(department_id)


@router.get("/", response_model=List[EmployeeRead])
async def get_employees(
        db_manager: DBManager = Depends(get_db_manager),
        session: AsyncSession = Depends(get_async_session)
):
    repo = db_manager.get_employee_repo(session)
    return await repo.get_all()
