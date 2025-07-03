from typing import TypeVar, Generic, List, Type

Entity = TypeVar("Entity")
Model = TypeVar("Model")

class BaseTranslator(Generic[Entity, Model]):
    entity: Type[Entity]
    model: Type[Model]

    def to_model(self, obj: Entity) -> Model:
        return self.model.model_validate(obj, from_attributes=True)

    def to_entity(self, obj: Model) -> Entity:
        raise NotImplementedError

    def to_model_many(self, objs: List[Entity]) -> List[Model]:
        return [self.to_model(obj) for obj in objs]

    def to_entity_many(self, objs: List[Model]) -> List[Entity]:
        return [self.to_entity(obj) for obj in objs]