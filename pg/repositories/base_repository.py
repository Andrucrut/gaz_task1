from typing import Generic, TypeVar, Type, List, Optional, Any
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from pg.translators.base_translator import BaseTranslator

Model = TypeVar("Model")
PydanticModel = TypeVar("PydanticModel")

class BaseRepository(Generic[Model, PydanticModel]):
    def __init__(self, session: AsyncSession, model: Type[Model], translator: BaseTranslator):
        self.session = session
        self.model = model
        self.translator = translator

    async def get(self, obj_id: Any) -> Optional[PydanticModel]:
        result = await self.session.execute(select(self.model).where(self.model.id == obj_id))
        orm_obj = result.scalar_one_or_none()
        if orm_obj is None:
            return None
        return self.translator.to_model(orm_obj)

    async def get_all(self) -> List[PydanticModel]:
        result = await self.session.execute(select(self.model))
        orm_objs = result.scalars().all()
        return self.translator.to_model_many(orm_objs)

    async def add(self, obj: Model) -> PydanticModel:
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return self.translator.to_model(obj)

    async def update(self, obj_id: Any, **kwargs) -> Optional[PydanticModel]:
        result = await self.session.execute(select(self.model).where(self.model.id == obj_id))
        obj = result.scalar_one_or_none()
        if not obj:
            return None
        for key, value in kwargs.items():
            setattr(obj, key, value)
        await self.session.commit()
        await self.session.refresh(obj)
        return self.translator.to_model(obj)

    async def delete(self, obj_id: Any) -> bool:
        result = await self.session.execute(select(self.model).where(self.model.id == obj_id))
        obj = result.scalar_one_or_none()
        if not obj:
            return False
        await self.session.delete(obj)
        await self.session.commit()
        return True