from datetime import datetime
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
        result_class = inspect(result).class_
        result_relationships = inspect(result_class).relationships
        for key, relation_property in result_relationships.items():
            if (
                not options_dict
                or "relations" not in options_dict
                or key not in options_dict["relations"]
            ):
                for (
                    referred_repository,
                    f_key,
                    value,
                ) in self.__get_repository_from_foreign_keys(result.__dict__):
                    if value:
                        _entity = await referred_repository.find_one(str(value), db)

                        if _entity is None:
                            setattr(result, f_key, None)

            else:
                if getattr(result, key):
                    column = DatabaseUtils.get_column_represent_deleted(get_columns(result_class))
                    if not isinstance(getattr(result, key), list):
                        if getattr(getattr(result, key), column.description):
                            setattr(result, key, None)
                        else:
                            new_result_key = await self.__remove_deleted_relations(
                                db, getattr(result, key), options_dict
                            )
                            setattr(result, key, new_result_key)
                    else:
                        for index, element in enumerate(getattr(result, key)):
                            if getattr(element, column.description):
                                del getattr(result, key)[index]
                            else:
                                new_result_key = await self.__remove_deleted_relations(
                                    db, element, options_dict
                                )
                                getattr(result, key)[index] = new_result_key

        return result

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

    @staticmethod
    def __get_cascade_relations(entity: T) -> List[Any]:
        cascade_relations = []

        for relation in inspect(inspect(entity).class_).relationships:
            delete_column = DatabaseUtils.get_column_represent_deleted(
                get_columns(relation.mapper.class_)
            )
            if delete_column is None:
                raise ValueError(f'Relation "{relation.key}" has no "deleted" column')

            cr = getattr(entity, relation.key)
            if cr and relation.cascade.delete_orphan:
                if not isinstance(cr, List):
                    cr = [cr]

                cascade_relations.extend(
                    cascade_relation
                    for cascade_relation in cr
                    if not getattr(cascade_relation, delete_column.name, True)
                )

        return cascade_relations

    async def __soft_delete_cascade(
        self, criteria: Union[str, int, FindOneOptions], db: Session
    ) -> Optional[UpdateResult]:
        entity = await self.find_one_or_fail(criteria, db)

        rowcount = await self.__soft_delete_cascade_relations(entity, db)
        rowcount += self.__soft_delete_entity(entity, db)

        return UpdateResult(raw=[], affected=rowcount, generatedMaps=[])

    async def __soft_delete_cascade_relations(self, entity: T, db: Session) -> int:
        rowcount = 0

        cascade_entities = self.__get_cascade_relations(entity)
        for cascade_entity in cascade_entities:
            result = await BaseRepository(inspect(cascade_entity).class_).__soft_delete_cascade(
                str(cascade_entity.id), db
            )
            rowcount += result["affected"]

        return rowcount

    @staticmethod
    def __soft_delete_entity(entity: T, db: Session) -> int:
        entity_class = inspect(entity).class_
        delete_column = DatabaseUtils.get_column_represent_deleted(get_columns(entity_class))
        if delete_column is None:
            raise ValueError(f'Entity "{entity_class.__name__}" has no "deleted" column')

        if not getattr(entity, delete_column.name):
            setattr(entity, delete_column.name, datetime.now())
            db.flush()

            return 1

        return 0
