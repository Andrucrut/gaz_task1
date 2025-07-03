from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, AsyncEngine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os


load_dotenv()
DB_URL = os.getenv("DATABASE_URL")


Base = declarative_base()


class Database:
    def __init__(self, db_url: str = None):
        self.db_url = db_url or DB_URL
        self.engine: AsyncEngine = create_async_engine(self.db_url, echo=True)
        self.AsyncSessionLocal = sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
            expire_on_commit=False
        )

    async def get_session(self) -> AsyncSession:
        async with self.AsyncSessionLocal() as session:
            yield session

    async def create_all(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def drop_all(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)


DB = Database()
async def get_async_session():
    async for session in DB.get_session():
        yield session