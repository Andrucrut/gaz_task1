from pg.translators.base_translator import BaseTranslator
from src.entites.project import Project as ProjectEntity
from src.models.project_model import Project as ProjectModel, ProjectCreate


class ProjectTranslator(BaseTranslator[ProjectEntity, ProjectModel]):
    entity = ProjectEntity
    model = ProjectModel

    def to_entity(self, project_create: ProjectCreate) -> ProjectEntity:
        return ProjectEntity(
            name=project_create.name.strip(),
            description=project_create.description.strip(),
            start_date=project_create.start_date,
            end_date=project_create.end_date,
        )
