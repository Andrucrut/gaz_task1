from typing import Generic, TypeVar, Type, List, Optional, Any
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from pg.translators.base_translator import BaseTranslator

Entity = TypeVar("Entity")
Model = TypeVar("Model")

class BaseRepository(Generic[Entity, Model]):
    def __init__(self, session: AsyncSession, entity: Type[Entity], translator: BaseTranslator, model: Type[Model] = None):
        self.session = session
        self.entity = entity
        self.translator = translator
        self.model = model

    async def get(self, obj_id: Any) -> Optional[Model]:
        result = await self.session.execute(select(self.entity).where(self.entity.id == obj_id))
        entity_obj = result.scalar_one_or_none()
        if entity_obj is None:
            return None
        return self.translator.to_model(entity_obj)

    async def get_all(self) -> List[Model]:
        result = await self.session.execute(select(self.entity))
        entity_objs = result.scalars().all()
        return self.translator.to_model_many(entity_objs)

    async def add(self, obj: Entity) -> Model:
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return self.translator.to_model(obj)

    async def update(self, obj_id: Any, **kwargs) -> Optional[Model]:
        result = await self.session.execute(select(self.entity).where(self.entity.id == obj_id))
        obj = result.scalar_one_or_none()
        if not obj:
            return None
        for key, value in kwargs.items():
            setattr(obj, key, value)
        await self.session.commit()
        await self.session.refresh(obj)
        return self.translator.to_model(obj)

    async def delete(self, obj_id: Any) -> bool:
        result = await self.session.execute(select(self.entity).where(self.entity.id == obj_id))
        obj = result.scalar_one_or_none()
        if not obj:
            return False
        await self.session.delete(obj)
        await self.session.commit()
        return True