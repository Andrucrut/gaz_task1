from sqlalchemy.orm import Session

from pg.repositories.base_repository import BaseRepository
from pg.translators.projectTranslator import ProjectTranslator
from src.models.project import ProjectRead
from src.entites.project import Project


class ProjectRepository(BaseRepository[Project, ProjectRead]):
    def __init__(self, session: Session):
        super().__init__(session, Project, ProjectTranslator())