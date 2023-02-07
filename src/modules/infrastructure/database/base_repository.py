from typing import Any, Generic, List, Optional, Tuple, TypeVar, Union

from pydantic import BaseModel
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import Session
from sqlalchemy_utils import get_class_by_table, get_columns

from src.core.types.delete_result_type import DeleteResult
from src.core.types.exceptions_type import NotFoundException
from src.core.types.find_many_options_type import FindManyOptions
from src.core.types.find_one_options_type import FindOneOptions
from src.core.types.update_result_type import UpdateResult
from src.core.utils.database_utils import DatabaseUtils
from . import get_db
from .base import Base
from .repository_methods.query_constructor import QueryConstructor
from .repository_methods.soft_delete import SoftDelete
from .repository_methods.soft_delete_filter import pause_listener

T = TypeVar("T")


class BaseRepository(Generic[T]):
    entity: T = None

    def __init__(self, entity: T):
        self.entity = entity
        self.query_constructor = QueryConstructor(entity)

    # ----------- PUBLIC METHODS -----------
    async def find(
        self, options_dict: FindManyOptions = None, db: Session = next(get_db())
    ) -> Optional[List[T]]:
        with pause_listener.pause(options_dict):
            query = self.query_constructor.build_query(db, options_dict)
            result = query.all()

            if (
                result
                and not DatabaseUtils.is_with_deleted_data(options_dict)
                and DatabaseUtils.should_apply_filter(
                    query, DatabaseUtils.get_column_represent_deleted(get_columns(self.entity))
                )
            ):
                result = [
                    await self.__remove_deleted_relations(db, element, options_dict)
                    for element in result
                ]

            return result

    async def find_and_count(
        self, options_dict: FindManyOptions = None, db: Session = next(get_db())
    ) -> Optional[Tuple[List[T], int]]:
        with pause_listener.pause(options_dict):
            query = self.query_constructor.build_query(db, options_dict)
            count = query.offset(None).limit(None).count()
            result = query.all()

            if (
                result
                and not DatabaseUtils.is_with_deleted_data(options_dict)
                and DatabaseUtils.should_apply_filter(
                    query, DatabaseUtils.get_column_represent_deleted(get_columns(self.entity))
                )
            ):
                result = [
                    await self.__remove_deleted_relations(db, element, options_dict)
                    for element in result
                ]

            return result, count

    async def find_one(self, criteria: Union[str, int, FindOneOptions], db: Session) -> Optional[T]:
        with_deleted = (
            DatabaseUtils.is_with_deleted_data(criteria)
            if not isinstance(criteria, (str, int))
            else False
        )

        with pause_listener.pause(with_deleted):
            query = self.query_constructor.build_query(db, criteria)
            result = query.first()

            if (
                result
                and not with_deleted
                and DatabaseUtils.should_apply_filter(
                    query, DatabaseUtils.get_column_represent_deleted(get_columns(self.entity))
                )
            ):
                result = await self.__remove_deleted_relations(db, result, criteria)

            return result

    async def find_one_or_fail(
        self, criteria: Union[str, int, FindOneOptions], db: Session
    ) -> Optional[T]:
        result = await self.find_one(criteria, db)

        if not result:
            message = f'Could not find any entity of type "{self.entity.__name__}" that matches the criteria'
            raise NotFoundException(message, [self.entity.__name__])

        return result

    async def create(self, _entity: Union[T, BaseModel], db: Session) -> T:
        if isinstance(_entity, BaseModel):
            partial_data_entity = _entity.dict(exclude_unset=True)
            _entity = self.entity(**partial_data_entity)

        await self.__is_relations_valid(db, _entity.__dict__)

        db.add(_entity)
        db.flush()
        return _entity

    @staticmethod
    def save(_entity: Union[T, List[T]] = None, db: Session = next(get_db())) -> Optional[T]:
        db.commit()

        if _entity:
            BaseRepository.refresh_entity(_entity, db)
        return _entity

    async def delete(
        self, criteria: Union[str, int, FindOneOptions], db: Session
    ) -> Optional[DeleteResult]:
        entity = await self.find_one_or_fail(criteria, db)

        db.delete(entity)
        db.flush() if db.transaction.nested else db.commit()

        return DeleteResult(raw=[], affected=1)

    async def soft_delete(
        self, criteria: Union[str, int, FindOneOptions], db: Session
    ) -> Optional[UpdateResult]:
        try:
            response = await self.__soft_delete_cascade(criteria, db)
            db.flush() if db.transaction.nested else db.commit()
            return response

        except Exception as e:
            db.rollback()
            raise e

    async def update(
        self,
        criteria: Union[str, int, FindOneOptions],
        partial_entity: Union[BaseModel, dict],
        db: Session,
    ) -> Optional[UpdateResult]:
        entity = await self.find_one_or_fail(criteria, db)

        if isinstance(partial_entity, BaseModel):
            partial_entity = partial_entity.dict(exclude_unset=True)

        await self.__is_relations_valid(db, partial_entity)

        for key, value in partial_entity.items():
            setattr(entity, key, value)

        db.flush() if db.transaction.nested else db.commit()
        return UpdateResult(raw=[], affected=1, generatedMaps=[])

    @staticmethod
    def refresh_entity(entity: Union[T, List[T]], db: Session) -> Union[T, List[T]]:
        db.refresh(entity) if not isinstance(entity, List) else (db.refresh(_en) for _en in entity)
        return entity

    # ----------- PRIVATE METHODS -----------
    async def __remove_deleted_relations(
        self, db: Session, result: T, options_dict: FindManyOptions = None
    ) -> T:
        result_class = type(result)
        result_relationships = inspect(result_class).relationships

        for key, relation_property in result_relationships.items():
            if self.__should_remove_relation(key, options_dict):
                for referred_repository, f_key, value in self.__get_repository_from_foreign_keys(
                    result.__dict__
                ):
                    if value:
                        _entity = await referred_repository.find_one(
                            str(value), db
                        )  # TODO: it's not necessary to use find_one, just write a query manually

                        if _entity is None:
                            setattr(result, f_key, None)

            else:
                if getattr(result, key):
                    await self.__remove_deleted_relations_from_attribute(
                        db, result, key, options_dict
                    )

        return result

    @staticmethod
    def __should_remove_relation(relation_key: str, options_dict: FindManyOptions) -> bool:
        if not options_dict or "relations" not in options_dict:
            return True

        return relation_key not in options_dict["relations"]

    async def __remove_deleted_relations_from_attribute(
        self, db: Session, result: T, attribute_key: str, options_dict: FindManyOptions
    ) -> None:
        attribute_value = getattr(result, attribute_key)
        if not isinstance(attribute_value, list):
            await self.__remove_deleted_relations_from_single_value(
                db, result, attribute_key, options_dict
            )
        else:
            await self.__remove_deleted_relations_from_list(result, attribute_key)

    async def __remove_deleted_relations_from_single_value(
        self, db: Session, result: T, attribute_key: str, options_dict: FindManyOptions
    ) -> None:
        single_value = getattr(result, attribute_key)
        if DatabaseUtils.is_deleted(single_value):
            setattr(result, attribute_key, None)
        else:
            new_result_key = await self.__remove_deleted_relations(db, single_value, options_dict)
            setattr(result, attribute_key, new_result_key)

    @staticmethod
    async def __remove_deleted_relations_from_list(result: T, attribute_key: str) -> None:
        attribute_list = getattr(result, attribute_key)
        # new_list = [
        #     await self.__remove_deleted_relations(db, element, options_dict)
        #     for element in attribute_list
        #     if not DatabaseUtils.is_deleted(element)
        # ]
        new_list = [element for element in attribute_list if not DatabaseUtils.is_deleted(element)]

        setattr(result, attribute_key, new_list)

    def __get_repository_from_foreign_keys(
        self, entity_data: Union[BaseModel, dict]
    ) -> List[Tuple["BaseRepository", str, Any]]:
        foreign_keys = {
            column.key: column for column in get_columns(self.entity) if column.foreign_keys
        }

        for key, value in entity_data.items():
            if key in foreign_keys:
                referred_table = next(
                    iter(foreign_keys[key].foreign_keys)
                ).constraint.referred_table

                referred_repository = BaseRepository(get_class_by_table(Base, referred_table))
                yield referred_repository, key, value

    async def __is_relations_valid(
        self, db: Session, partial_entity: Union[BaseModel, dict]
    ) -> bool:
        foreign_keys = {
            column.key: column for column in get_columns(self.entity) if column.foreign_keys
        }

        for referred_repository, key, value in self.__get_repository_from_foreign_keys(
            partial_entity
        ):
            if not value and foreign_keys[key].nullable:
                continue
            await referred_repository.find_one_or_fail(str(value), db)

        return True

    async def __soft_delete_cascade(
        self, criteria: Union[str, int, FindOneOptions], db: Session
    ) -> Optional[UpdateResult]:
        entity = await self.find_one_or_fail(criteria, db)

        rowcount = await self.__soft_delete_cascade_relations(entity, db)
        rowcount += SoftDelete.soft_delete_entity(entity, db)

        return UpdateResult(raw=[], affected=rowcount, generatedMaps=[])

    @staticmethod
    async def __soft_delete_cascade_relations(entity: T, db: Session) -> int:
        rowcount = 0

        cascade_entities = DatabaseUtils.get_cascade_relations(entity)
        for cascade_entity in cascade_entities:
            result = await BaseRepository(inspect(cascade_entity).class_).__soft_delete_cascade(
                str(cascade_entity.id), db
            )
            rowcount += result["affected"]

        return rowcount
