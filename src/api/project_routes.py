from fastapi import APIRouter, Depends
from typing import List

from src.models.project_model import Project, ProjectCreate, ProjectUpdate,ProjectRead
from pg.manager import DBManager
from pg.dependencies import get_db_manager

router = APIRouter(prefix="/projects", tags=["project"])


@router.post("/", response_model=ProjectRead)
async def create_project(
        project: ProjectCreate,
        db_manager: DBManager = Depends(get_db_manager)
):
    return await db_manager.project_repo.add_model(project)


@router.get("/", response_model=List[ProjectRead])
async def get_projects(
        db_manager: DBManager = Depends(get_db_manager)

):
    return await db_manager.project_repo.get_all()



