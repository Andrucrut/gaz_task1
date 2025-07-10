import uuid

from pydantic import BaseModel, Field


class TaskId(BaseModel):
    value: uuid.UUID = Field(validation_alias="id")
