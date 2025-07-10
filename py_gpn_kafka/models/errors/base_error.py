from pydantic import BaseModel, Field


class BaseError(BaseModel):
    message: str = Field(default="Something went wrong", description="error message")
    type: str = Field(default="Error", description="error type")
