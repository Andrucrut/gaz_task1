from typing import TypeVar, Generic, List, Type

Model = TypeVar("Model")
PydanticModel = TypeVar("PydanticModel")

class BaseTranslator(Generic[Model, PydanticModel]):
    orm_model: Type[Model]
    pydantic_model: Type[PydanticModel]

    def to_model(self, obj: Model) -> PydanticModel:
        return self.pydantic_model.model_validate(obj, from_attributes=True)

    def to_entity(self, obj: PydanticModel) -> Model:
        raise NotImplementedError

    def to_model_many(self, objs: List[Model]) -> List[PydanticModel]:
        return [self.to_model(obj) for obj in objs]

    def to_entity_many(self, objs: List[PydanticModel]) -> List[Model]:
        return [self.to_entity(obj) for obj in objs]