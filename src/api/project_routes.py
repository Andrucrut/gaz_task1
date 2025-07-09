from fastapi import APIRouter, Depends
from typing import List
from pg.settings import get_db_manager, get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.project_model import ProjectCreate, ProjectRead
from pg.manager import DBManager

router = APIRouter(prefix="/projects", tags=["project"])


@router.post("/", response_model=ProjectRead)
async def create_project(
        project: ProjectCreate,
        db_manager: DBManager = Depends(get_db_manager),
        session: AsyncSession = Depends(get_async_session)
):
    repo = db_manager.get_project_repo(session)
    return await repo.add_model(project)


@router.get("/", response_model=List[ProjectRead])
async def get_projects(
        db_manager: DBManager = Depends(get_db_manager),
        session: AsyncSession = Depends(get_async_session)
):
    repo = db_manager.get_project_repo(session)
    return await repo.get_all()
