from pydantic.v1 import BaseSettings
from sqlalchemy.orm import declarative_base
from .connection import Database

class Settings(BaseSettings):
    DATABASE_URL: str

    class Config:
        env_file = ".env"

settings = Settings()

Base = declarative_base()

DB = Database(settings.DATABASE_URL, Base)
AsyncSessionLocal = DB.AsyncSessionLocal

async def get_async_session():
    async for session in DB.get_session():
        yield session

def get_db_manager():
    from .manager import DBManager
    return DBManager()