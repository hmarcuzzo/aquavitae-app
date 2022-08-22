from datetime import datetime
from typing import Any, Generic, List, Optional, Tuple, TypeVar, Union

from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import Query, Session, subqueryload
from sqlalchemy_utils import get_class_by_table, get_columns

from src.core.types.delete_result_type import DeleteResult
from src.core.types.exceptions_type import BadRequestException, NotFoundException
from src.core.types.find_many_options_type import FindManyOptions
from src.core.types.find_one_options_type import FindOneOptions
from src.core.types.update_result_type import UpdateResult
from src.core.utils.database_utils import DatabaseUtils
from . import get_db
from .base import Base
from .soft_delete_filter import pause_listener

T = TypeVar("T")


class BaseRepository(Generic[T]):
    entity: T = None

    def __init__(self, entity: T):
        self.entity = entity
        self.with_deleted = False

    # ----------- PRIVATE METHODS -----------
    def __apply_options(
        self, query: Query, options_dict: Union[FindManyOptions, FindManyOptions] = None
    ) -> Query:
        if not options_dict:
            return query

        options_dict = self.__fix_options_dict(options_dict)
        query = query.enable_assertions(False)

        for key in options_dict.keys():
            if key == "where":
                query = query.where(*options_dict["where"])
            elif key == "order_by":
                query = query.order_by(*options_dict["order_by"])
            elif key == "skip":
                query = query.offset(options_dict["skip"])
            elif key == "take":
                query = query.limit(options_dict["take"])
            elif key == "relations":
                query = query.options(
                    subqueryload(getattr(self.entity, *options_dict["relations"]))
                )
            elif key == "with_deleted":
                self.with_deleted = options_dict["with_deleted"]
            else:
                raise KeyError(f"Unknown option: {key} in FindOptions")

        return query

    @staticmethod
    def __fix_options_dict(
        options_dict: Union[FindManyOptions, FindOneOptions]
    ) -> Union[FindManyOptions, FindOneOptions]:
        for attribute in ["where", "order_by", "options"]:
            if attribute in options_dict and not isinstance(options_dict[attribute], list):
                options_dict[attribute] = [options_dict[attribute]]

        return options_dict

    def __generate_find_one_options_dict(self, criteria: Union[str, int]) -> FindOneOptions:
        return {"where": [inspect(self.entity).primary_key[0] == criteria]}

    def __get_repository_from_foreign_keys(
        self, entity_data: Union[BaseModel, dict]
    ) -> List[Tuple["BaseRepository", str, Any]]:
        columns = get_columns(self.entity)

        for key, value in entity_data.items():
            if key in columns and columns[key].foreign_keys:
                referred_table = next(iter(columns[key].foreign_keys)).constraint.referred_table

                referred_repository = BaseRepository(get_class_by_table(Base, referred_table))
                yield referred_repository, key, value

    async def __is_relations_valid(
        self, db: Session, partial_entity: Union[BaseModel, dict]
    ) -> bool:
        columns = get_columns(self.entity)

        for referred_repository, key, value in self.__get_repository_from_foreign_keys(
            partial_entity
        ):
            if not value and columns[key].nullable:
                continue
            await referred_repository.find_one_or_fail(str(value), db)

        return True

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
                for referred_repository, f_key, value in self.__get_repository_from_foreign_keys(
                    result.__dict__
                ):
                    if value:
                        _entity = await referred_repository.find_one(str(value), db)

                        if _entity is None:
                            setattr(result, f_key, None)

            else:
                if getattr(result, key):
                    column = DatabaseUtils.get_column_represent_deleted(get_columns(result_class))
                    if getattr(getattr(result, key), column.description):
                        setattr(result, key, None)
                    else:
                        new_result_key = await self.__remove_deleted_relations(
                            db, getattr(result, key), options_dict
                        )
                        setattr(result, key, new_result_key)

        return result

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
            if cr:
                if not isinstance(cr, List):
                    cr = [cr]

                for cascade_relation in cr:
                    if relation.cascade.delete_orphan and not getattr(
                        cascade_relation,
                        delete_column.name,
                    ):
                        cascade_relations.append(cascade_relation)

        return cascade_relations

    async def __soft_delete_cascade_relations(self, entity: T, db: Session) -> int:
        rowcount = 0

        cascade_entities = self.__get_cascade_relations(entity)
        for cascade_entity in cascade_entities:
            result = await BaseRepository(inspect(cascade_entity).class_).__soft_delete_cascade(
                str(cascade_entity.id), db
            )
            rowcount = result["affected"]

        return rowcount

    @staticmethod
    def __soft_delete_entity(entity: T, db: Session) -> int:
        entity_class = inspect(entity).class_
        delete_column = DatabaseUtils.get_column_represent_deleted(get_columns(entity_class))
        if delete_column is None:
            raise ValueError(f'Entity "{entity_class.__name__}" has no "deleted" column')

        if not getattr(entity, delete_column.name):
            setattr(entity, delete_column.name, datetime.now())
            db.commit()

            return 1

        return 0

    async def __soft_delete_cascade(
        self, criteria: Union[str, int, FindOneOptions], db: Session
    ) -> Optional[UpdateResult]:
        entity = await self.find_one_or_fail(criteria, db)

        rowcount = await self.__soft_delete_cascade_relations(entity, db)
        rowcount += self.__soft_delete_entity(entity, db)

        return UpdateResult(raw=[], affected=rowcount, generatedMaps=[])

    # ----------- PUBLIC METHODS -----------
    async def find(
        self, options_dict: FindManyOptions = None, db: Session = next(get_db())
    ) -> Optional[List[T]]:
        query = db.query(self.entity)

        query = self.__apply_options(query, options_dict)
        with pause_listener.pause(self.with_deleted):
            result = query.all()

            if (
                result
                and not self.with_deleted
                and DatabaseUtils.should_apply_filter(
                    query, DatabaseUtils.get_column_represent_deleted(get_columns(self.entity))
                )
            ):
                result = [
                    await self.__remove_deleted_relations(db, element, options_dict)
                    for element in result
                ]

            self.with_deleted = False
            return result

    async def find_and_count(
        self, options_dict: FindManyOptions = None, db: Session = next(get_db())
    ) -> Optional[Tuple[List[T], int]]:
        query = db.query(self.entity)

        query = self.__apply_options(query, options_dict)
        with pause_listener.pause(self.with_deleted):
            count = query.offset(None).limit(None).count()
            result = query.all()

            if (
                result
                and not self.with_deleted
                and DatabaseUtils.should_apply_filter(
                    query, DatabaseUtils.get_column_represent_deleted(get_columns(self.entity))
                )
            ):
                result = [
                    await self.__remove_deleted_relations(db, element, options_dict)
                    for element in result
                ]

            self.with_deleted = False
            return result, count

    async def find_one(
        self, criteria: Union[str, int, FindOneOptions], db: Session = next(get_db())
    ) -> Optional[T]:
        query = db.query(self.entity)

        if isinstance(criteria, (str, int)):
            criteria = self.__generate_find_one_options_dict(criteria)
        query = self.__apply_options(query, criteria)

        with pause_listener.pause(self.with_deleted):
            result = query.first()

            if (
                result
                and not self.with_deleted
                and DatabaseUtils.should_apply_filter(
                    query, DatabaseUtils.get_column_represent_deleted(get_columns(self.entity))
                )
            ):
                result = await self.__remove_deleted_relations(db, result, criteria)

            self.with_deleted = False
            return result

    async def find_one_or_fail(
        self, criteria: Union[str, int, FindOneOptions], db: Session = next(get_db())
    ) -> Optional[T]:
        result = await self.find_one(criteria, db)

        if not result:
            message = f'Could not find any entity of type "{self.entity.__name__}" that matches the criteria'
            raise NotFoundException(message, [self.entity.__name__])

        return result

    async def create(self, _entity: Union[T, BaseModel], db: Session = next(get_db())) -> T:
        if isinstance(_entity, BaseModel):
            partial_data_entity = _entity.dict(exclude_unset=True)
            _entity = self.entity(**partial_data_entity)

        await self.__is_relations_valid(db, _entity.__dict__)

        db.add(_entity)
        return _entity

    @staticmethod
    async def save(_entity: T, db: Session = next(get_db())) -> Optional[T]:
        db.commit()
        db.refresh(_entity)
        return _entity

    async def delete(
        self, criteria: Union[str, int, FindOneOptions], db: Session = next(get_db())
    ) -> Optional[DeleteResult]:
        entity = await self.find_one_or_fail(criteria, db)

        db.delete(entity)
        db.commit()

        return DeleteResult(raw=[], affected=1)

    async def soft_delete(
        self, criteria: Union[str, int, FindOneOptions], db: Session = next(get_db())
    ) -> Optional[UpdateResult]:
        try:
            db.begin_nested()
            response = await self.__soft_delete_cascade(criteria, db)
            db.commit()
            return response

        except Exception as e:
            db.rollback()
            raise e

    async def update(
        self,
        criteria: Union[str, int, FindOneOptions],
        partial_entity: Union[BaseModel, dict],
        db: Session = next(get_db()),
    ) -> Optional[UpdateResult]:
        entity = await self.find_one_or_fail(criteria, db)

        if isinstance(partial_entity, BaseModel):
            partial_entity = partial_entity.dict(exclude_unset=True)

        await self.__is_relations_valid(db, partial_entity)

        for key, value in partial_entity.items():
            setattr(entity, key, value)

        db.commit()
        return UpdateResult(raw=[], affected=1, generatedMaps=[])
