from fastapi import APIRouter, Depends, HTTPException
from typing import List

from src.models.department_model import DepartmentCreate, DepartmentRead, DepartmentUpdate
from src.models.employee_model import EmployeeRead
from pg.manager import DBManager
from pg.dependencies import get_db_manager

router = APIRouter(prefix="/departments", tags=["departments"])

@router.post("/", response_model=DepartmentRead)
async def create_department(
    department: DepartmentCreate,
    db_manager: DBManager = Depends(get_db_manager)
):
    return await db_manager.department_repo.add_model(department)


@router.get("/{department_id}/employees", response_model=List[EmployeeRead])
async def get_employees_by_department(
    department_id: int,
    db_manager: DBManager = Depends(get_db_manager)
):
    return await db_manager.employee_repo.get_employees_by_department(department_id)


@router.get("/", response_model=List[DepartmentRead])
async def get_all_departments(
    db_manager: DBManager = Depends(get_db_manager)
):
    return await db_manager.department_repo.get_all()


@router.put("/{department_id}", response_model=DepartmentRead)
async def update_department(
    department_id: int,
    department: DepartmentUpdate,
    db_manager: DBManager = Depends(get_db_manager)
):
    updated_department = await db_manager.department_repo.update_model(department_id, department)
    if not updated_department:
        raise HTTPException(status_code=404, detail="Department not found")
    return updated_department


@router.delete("/{department_id}")
async def delete_department(
    department_id: int,
    db_manager: DBManager = Depends(get_db_manager)
):
    success = await db_manager.department_repo.delete(department_id)
    if not success:
        raise HTTPException(status_code=404, detail="Department not found")
    return {"ok": True}


@router.get("/{department_id}", response_model=DepartmentRead)
async def get_department_by_id(
    department_id: int,
    db_manager: DBManager = Depends(get_db_manager)
):
    department = await db_manager.department_repo.get_by_id(department_id)
    if not department:
        raise HTTPException(status_code=404, detail="Department not found")
    return department