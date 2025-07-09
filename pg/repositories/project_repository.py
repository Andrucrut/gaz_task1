from sqlalchemy.orm import Session

from pg.repositories.base_repository import BaseRepository
from pg.translators.project_translator import ProjectTranslator
from src.models.project_model import ProjectRead
from src.entites.project import Project


class ProjectRepository(BaseRepository[Project, ProjectRead]):
    def __init__(self, session: Session):
        super().__init__(session, Project, ProjectTranslator())