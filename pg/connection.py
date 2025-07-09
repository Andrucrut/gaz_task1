from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, AsyncEngine
from sqlalchemy.orm import sessionmaker


class Database:
    def __init__(self, db_url: str, base):
        self.db_url = db_url
        self.base = base
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
            await conn.run_sync(self.base.metadata.create_all)

    async def drop_all(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(self.base.metadata.drop_all)
