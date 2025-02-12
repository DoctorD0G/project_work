from abc import ABC, abstractmethod
from enum import Enum
from typing import (
    Generic,
    TypeVar,
    Type,
    Any,
    Callable,
    AsyncContextManager,
    Tuple,
    Union,
)
from typing import Optional

import pymongo
from bson import ObjectId
from fastapi_pagination import Params
from fastapi_pagination.ext.motor import paginate as motor_paginate
from fastapi_pagination.ext.sqlalchemy import paginate
from motor.motor_asyncio import AsyncIOMotorCollection
from pydantic import BaseModel, Field
from sqlalchemy import select, delete, TextClause
from sqlalchemy.exc import IntegrityError, MultipleResultsFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import Select, text

from domain.entities.common import EntityId, Total
from domain.exceptions import DbObjExistsException, MultipleResultException

ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
EntityType = TypeVar("EntityType", bound=BaseModel)


class FilterOperator(str, Enum):
    EQ = "eq"  # Равенство (equality)
    NE = "ne"  # Неравенство (not equal)
    GT = "gt"  # Больше чем (greater than)
    LT = "lt"  # Меньше чем (less than)
    GTE = "gte"  # Больше или равно (greater than or equal)
    LTE = "lte"  # Меньше или равно (less than or equal)
    LIKE = "like"  # LIKE оператор
    ILIKE = "ilike"  # ILIKE оператор (регистронезависимый LIKE)
    IN = "in"  # IN оператор


class FieldFilter(BaseModel):
    field: str
    operator: FilterOperator
    value: Any

    class Config:
        arbitrary_types_allowed = True


class Filter(BaseModel):
    filters: list[FieldFilter] = Field(default_factory=list)

    class Config:
        arbitrary_types_allowed = True


class AbstractRepository(
    ABC, Generic[ModelType, CreateSchemaType, UpdateSchemaType, EntityType]
):
    @abstractmethod
    def convert_model_to_entity(self, model: ModelType) -> EntityType:
        pass

    @abstractmethod
    async def create(self, obj_in: CreateSchemaType) -> EntityType:
        pass

    @abstractmethod
    async def get(self, id: EntityId) -> EntityType | None:
        pass

    @abstractmethod
    async def get_one_by_filter(self, filter: Filter) -> EntityType | None:
        pass

    @abstractmethod
    async def update(self, id: EntityId, obj_in: UpdateSchemaType) -> EntityType | None:
        pass

    @abstractmethod
    async def delete(self, id: EntityId):
        pass

    @abstractmethod
    async def delete_by_filter(self, filter: Filter) -> int:
        pass

    @abstractmethod
    async def get_paginable_items(
        self,
        page: int,
        size: int,
        sort_field: str | None = None,
        sort_descending: bool | None = None,
        filter: Filter | None = None,
    ) -> Tuple[list[EntityType], Total]:
        pass

    @abstractmethod
    async def get_filtered_items(
        self,
        sort_field: str | None = None,
        sort_descending: bool | None = None,
        filter: Filter | None = None,
        limit: int | None = None,
    ) -> list[EntityType]:
        pass


class SQLAlchemyRepository(
    AbstractRepository[ModelType, CreateSchemaType, UpdateSchemaType, EntityType]
):
    session_contextmanager: Callable[..., AsyncContextManager[AsyncSession]] = None

    def __init__(
        self,
        session_contextmanager: Callable[..., AsyncContextManager[AsyncSession]],
        model: Type[ModelType],
        entity: Type[EntityType],
    ):
        super().__init__()
        self.session_contextmanager = session_contextmanager
        self.model = model
        self.entity = entity

    def get_psql_order_by_text(
        self, sort_field: Optional[str], sort_descending: bool = False
    ) -> Optional[TextClause]:
        if sort_field:
            descending = "desc" if sort_descending else "asc"
            return text(f"{sort_field} {descending}")
        else:
            return text("id desc")

    def convert_model_to_entity(self, model: ModelType) -> EntityType:
        return self.entity(**model.__dict__)

    async def create(self, obj_in: CreateSchemaType) -> EntityType:
        async with self.session_contextmanager() as db_session:
            try:
                obj_in_data = obj_in.dict()
                db_obj = self.model(**obj_in_data)
                db_session.add(db_obj)
                await db_session.commit()
                await db_session.refresh(db_obj)
                return self.convert_model_to_entity(db_obj)
            except IntegrityError as e:
                raise DbObjExistsException from e

    async def get(self, id: EntityId) -> EntityType | None:
        async with self.session_contextmanager() as db_session:
            query = select(self.model).filter(self.model.id == id)
            result = await db_session.execute(query)
            db_obj = result.scalar_one_or_none()
            return self.convert_model_to_entity(db_obj) if db_obj else None

    async def get_one_by_filter(self, filter: Filter) -> EntityType | None:
        async with self.session_contextmanager() as db_session:
            try:
                query = select(self.model)
                query = self._apply_filters(query, filter)
                result = await db_session.execute(query)
                db_obj = result.scalar_one_or_none()
                return self.convert_model_to_entity(db_obj) if db_obj else None
            except MultipleResultsFound as exc:
                raise MultipleResultException from exc

    async def update(self, id: Any, obj_in: UpdateSchemaType) -> EntityType | None:
        async with self.session_contextmanager() as db_session:
            query = select(self.model).filter(self.model.id == id)
            result = await db_session.execute(query)
            db_obj = result.scalar_one_or_none()

            if db_obj is None:
                return None

            # Преобразуем obj_in в словарь, исключая None значения
            update_data = obj_in.dict(exclude_unset=True)

            # Обновляем объект
            for field, value in update_data.items():
                setattr(db_obj, field, value)

            db_session.add(db_obj)
            await db_session.commit()
            await db_session.refresh(db_obj)
            return self.convert_model_to_entity(db_obj)

    async def delete(self, id: Any):
        async with self.session_contextmanager() as db_session:
            query = delete(self.model).where(self.model.id == id)
            await db_session.execute(query)
            await db_session.commit()

    async def delete_by_filter(self, filter: Filter) -> int:
        async with self.session_contextmanager() as db_session:
            query = delete(self.model)
            query = self._apply_filters(query, filter)
            result = await db_session.execute(query)
            await db_session.commit()
            return result.rowcount  # Возвращаем количество удаленных записей

    async def get_paginable_items(
        self,
        page: int,
        size: int,
        sort_field: str | None = None,
        sort_descending: bool | None = None,
        filter: Filter | None = None,
    ) -> Tuple[list[EntityType], Total]:
        async with self.session_contextmanager() as db_session:
            query = select(self.model)

            if filter:
                query = self._apply_filters(query, filter)

            ordering = [self.model.id.asc()]
            if sort_field:
                ordering = [self.get_psql_order_by_text(sort_field, sort_descending)]

            query = query.order_by(*ordering)

            pagination_params = Params(page=page, size=size)
            page_data = await paginate(db_session, query, pagination_params)

            results = []
            for db_obj in page_data.items:
                results.append(self.convert_model_to_entity(db_obj))

            return results, page_data.total

    async def get_filtered_items(
        self,
        sort_field: str | None = None,
        sort_descending: bool | None = None,
        filter: Filter | None = None,
        limit: int | None = None,
    ) -> list[EntityType]:
        async with self.session_contextmanager() as db_session:
            query = select(self.model)

            if filter:
                query = self._apply_filters(query, filter)

            ordering = [self.model.id.asc()]
            if sort_field:
                ordering = [self.get_psql_order_by_text(sort_field, sort_descending)]

            if limit:
                query = query.limit(limit)

            query = query.order_by(*ordering)

            result = await db_session.execute(query)

            results: list[EntityType] = []
            for db_obj in result.scalars().all():
                results.append(self.convert_model_to_entity(db_obj))

            return results

    def _apply_filters(
        self, query: Union[Select, delete], filter: Filter
    ) -> Union[Select, delete]:
        for field_filter in filter.filters:
            column = getattr(self.model, field_filter.field)
            operator = field_filter.operator
            value = field_filter.value

            if operator == FilterOperator.EQ:
                query = query.where(column == value)
            elif operator == FilterOperator.NE:
                query = query.where(column != value)
            elif operator == FilterOperator.GT:
                query = query.where(column > value)
            elif operator == FilterOperator.LT:
                query = query.where(column < value)
            elif operator == FilterOperator.GTE:
                query = query.where(column >= value)
            elif operator == FilterOperator.LTE:
                query = query.where(column <= value)
            elif operator == FilterOperator.LIKE:
                query = query.where(column.like(f"%{value}%"))
            elif operator == FilterOperator.ILIKE:
                query = query.where(column.ilike(f"%{value}%"))
            elif operator == FilterOperator.IN:
                query = query.where(column.in_(value))

        return query


class MongoRepository(
    Generic[ModelType, CreateSchemaType, UpdateSchemaType, EntityType]
):
    def __init__(
        self,
        model: Type[ModelType],
        collection: AsyncIOMotorCollection,
        entity: Type[EntityType],
    ):
        self.model = model
        self.collection = collection
        self.entity = entity

    def convert_model_to_entity(self, data: dict) -> EntityType:
        db_obj = self.model.parse_obj(data)
        return self.entity.parse_obj(db_obj.dict())

    async def create(self, obj_in: CreateSchemaType) -> EntityType:
        try:
            obj_in_data = obj_in.dict()
            result = await self.collection.insert_one(obj_in_data)
            return await self.get(result.inserted_id)
        except Exception as e:
            raise DbObjExistsException from e

    async def get(self, id: EntityId) -> EntityType | None:
        result = await self.collection.find_one({"_id": ObjectId(id)})
        return self.convert_model_to_entity(result) if result else None

    async def get_one_by_filter(self, filter: Filter) -> EntityType | None:
        try:
            query = self._build_query(filter)
            result = await self.collection.find_one(query)
            return self.convert_model_to_entity(result) if result else None
        except Exception as exc:
            raise MultipleResultException from exc

    async def update(self, id: EntityId, obj_in: UpdateSchemaType) -> EntityType | None:
        update_data = obj_in.dict(exclude_unset=True)
        result = await self.collection.find_one_and_update(
            {"_id": ObjectId(id)}, {"$set": update_data}, return_document=True
        )
        return self.convert_model_to_entity(result) if result else None

    async def delete(self, id: EntityId):
        await self.collection.delete_one({"_id": ObjectId(id)})

    async def delete_by_filter(self, filter: Filter) -> int:
        query = self._build_query(filter)
        result = await self.collection.delete_many(query)
        return result.deleted_count

    def get_sort_text(self, sort_field: Optional[str], sort_descending: bool = False):
        if sort_field:
            sort_field = "_id" if sort_field == "id" else sort_field

            descending = pymongo.DESCENDING if sort_descending else pymongo.ASCENDING
            return [(f"{sort_field}", descending)]
        else:
            return [("_id", pymongo.DESCENDING)]

    async def get_paginable_items(
        self,
        page: int,
        size: int,
        sort_field: str | None = None,
        sort_descending: bool | None = None,
        filter: Filter | None = None,
    ) -> Tuple[list[EntityType], Total]:
        query = self._build_query(filter) if filter else {}
        sort = self.get_sort_text(sort_field, sort_descending)

        pagination_params = Params(page=page, size=size)
        page_data = await motor_paginate(
            self.collection, query, pagination_params, sort=sort
        )

        results = [self.convert_model_to_entity(item) for item in page_data.items]
        return results, page_data.total

    async def get_filtered_items(
        self,
        sort_field: str | None = None,
        sort_descending: bool | None = None,
        filter: Filter | None = None,
        limit: int | None = None,
    ) -> list[EntityType]:
        query = self._build_query(filter) if filter else {}
        sort = (
            [(sort_field, -1 if sort_descending else 1)] if sort_field else [("_id", 1)]
        )

        cursor = self.collection.find(query).sort(sort)
        if limit:
            cursor = cursor.limit(limit)

        results = [self.convert_model_to_entity(item) async for item in cursor]
        return results

    def _build_query(self, filter: Filter) -> dict:
        query = {}

        for field_filter in filter.filters:
            field = field_filter.field
            operator = field_filter.operator
            value = field_filter.value

            if operator == FilterOperator.EQ:
                query[field] = value
            elif operator == FilterOperator.NE:
                query[field] = {"$ne": value}
            elif operator == FilterOperator.GT:
                query[field] = {"$gt": value}
            elif operator == FilterOperator.LT:
                query[field] = {"$lt": value}
            elif operator == FilterOperator.GTE:
                query[field] = {"$gte": value}
            elif operator == FilterOperator.LTE:
                query[field] = {"$lte": value}
            elif operator == FilterOperator.IN:
                query[field] = {"$in": value}
            elif operator == FilterOperator.LIKE:
                query[field] = {"$regex": value, "$options": ""}
            elif operator == FilterOperator.ILIKE:
                query[field] = {"$regex": value, "$options": "i"}

        return query
