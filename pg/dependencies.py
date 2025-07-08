from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pg.connection import get_async_session
from pg.manager import DBManager


async def get_db_manager(session: AsyncSession = Depends(get_async_session)) -> DBManager:
    return DBManager(session)