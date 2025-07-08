from fastapi import APIRouter, Depends
from typing import List
from pg.dependencies import get_db_manager

from src.models.project_model import Project, ProjectCreate, ProjectUpdate, ProjectRead
from pg.manager import DBManager

router = APIRouter(prefix="/projects", tags=["project"])


@router.post("/", response_model=ProjectRead)
async def create_project(
    project: ProjectCreate,
    db_manager: DBManager = Depends(get_db_manager)
):
    async for repo in db_manager.get_project_repo():
        return await repo.add_model(project)


@router.get("/", response_model=List[ProjectRead])
async def get_projects(
    db_manager: DBManager = Depends(get_db_manager)
):
    async for repo in db_manager.get_project_repo():
        return await repo.get_all()