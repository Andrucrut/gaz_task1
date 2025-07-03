from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from src.models.employeeModel import EmployeeCreate, Employee as EmployeeModel
from pg.connection import get_async_session
from pg.repositories.employeeRepository import EmployeeRepository
from pg.translators.employeeTranslator import EmployeeTranslator

router = APIRouter(prefix="/employees", tags=["employees"])

translator = EmployeeTranslator()

@router.post("/", response_model=EmployeeModel)
async def create_employee(employee: EmployeeCreate, db: AsyncSession = Depends(get_async_session)):
    repo = EmployeeRepository(db)
    employee_entity = translator.to_entity(employee)
    employee_model = await repo.add(employee_entity)
    return employee_model

@router.get("/by_department/{department_id}", response_model=List[EmployeeModel])
async def get_employees_by_department(department_id: int, db: AsyncSession = Depends(get_async_session)):
    repo = EmployeeRepository(db)
    employees = await repo.get_employees_by_department(department_id)
    return employees

@router.get("/", response_model=List[EmployeeModel])
async def get_employees(db: AsyncSession = Depends(get_async_session)):
    repo = EmployeeRepository(db)
    employees = await repo.get_all()
    return employees