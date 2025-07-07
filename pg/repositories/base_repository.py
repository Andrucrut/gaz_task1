from typing import Generic, TypeVar, Type, List, Optional, Any
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from pg.translators.base_translator import BaseTranslator

Entity = TypeVar("Entity")
Model = TypeVar("Model")

class BaseRepository(Generic[Entity, Model]):
    def __init__(self, session: AsyncSession, entity: Type[Entity], translator: BaseTranslator):
        self.session = session
        self.entity = entity
        self.translator = translator

    async def get(self, obj_id: Any) -> Optional[Model]:
        result = await self.session.execute(
            select(self.entity).where(getattr(self.entity, 'id') == obj_id)
        )
        entity_obj = result.scalar_one_or_none()
        if entity_obj is None:
            return None
        return self.translator.to_model(entity_obj)

    async def get_all(self) -> List[Model]:
        result = await self.session.execute(select(self.entity))
        entity_objs = list(result.scalars().all())
        return self.translator.to_model_many(entity_objs)

    async def add_model(self, model: Model) -> Model:
        entity = self.translator.to_entity(model)
        self.session.add(entity)
        await self.session.commit()
        await self.session.refresh(entity)
        return self.translator.to_model(entity)

    async def update_model(self, obj_id: Any, model: Model) -> Optional[Model]:
        result = await self.session.execute(
            select(self.entity).where(getattr(self.entity, 'id') == obj_id)
        )
        entity = result.scalar_one_or_none()
        if not entity:
            return None

        update_data = model.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(entity, key, value)

        await self.session.commit()
        await self.session.refresh(entity)
        return self.translator.to_model(entity)

    async def delete(self, obj_id: Any) -> bool:
        result = await self.session.execute(
            select(self.entity).where(getattr(self.entity, 'id') == obj_id)
        )
        obj = result.scalar_one_or_none()
        if not obj:
            return False
        await self.session.delete(obj)
        await self.session.commit()
        return True
