from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from src.models.departmentModel import DepartmentCreate, DepartamentRead
from src.models.employeeModel import EmployeeRead
from pg.connection import get_async_session
from pg.repositories.departmentRepository import DepartmentRepository
from pg.repositories.employeeRepository import EmployeeRepository
from pg.translators.departmentTranslator import DepartmentTranslator
from pg.translators.employeeTranslator import EmployeeTranslator

router = APIRouter(prefix="/departments", tags=["departments"])

department_translator = DepartmentTranslator()
employee_translator = EmployeeTranslator()

@router.post("/", response_model=DepartamentRead)
async def create_department(department: DepartmentCreate, db: AsyncSession = Depends(get_async_session)):
    repo = DepartmentRepository(db)
    department_entity = department_translator.to_entity(department)
    department_model = await repo.add(department_entity)
    return department_model

@router.get("/{department_id}/employees", response_model=List[EmployeeRead])
async def get_employees_by_department(department_id: int, db: AsyncSession = Depends(get_async_session)):
    repo = EmployeeRepository(db)
    employees = await repo.get_employees_by_department(department_id)
    return employees

@router.get("/", response_model=List[DepartamentRead])
async def get_all_departments(db: AsyncSession = Depends(get_async_session)):
    repo = DepartmentRepository(db)
    departments = await repo.get_all()
    return departments

@router.delete("/{department_id}")
async def delete_department(department_id: int, db: AsyncSession = Depends(get_async_session)):
    repo = DepartmentRepository(db)
    success = await repo.delete(department_id)
    if not success:
        raise HTTPException(status_code=404, detail="Department not found")
    return {"ok": True} 