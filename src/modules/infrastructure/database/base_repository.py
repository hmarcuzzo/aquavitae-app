from datetime import datetime
from typing import List, Optional, Tuple, Union

from pydantic import BaseModel
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import DeclarativeMeta, lazyload, Query, Session
from sqlalchemy_utils import get_columns

from src.core.types.delete_result_type import DeleteResult
from src.core.types.exceptions_type import InternalServerError, NotFoundException
from src.core.types.find_many_options_type import FindManyOptions
from src.core.types.find_one_options_type import FindOneOptions
from src.core.types.update_result_type import UpdateResult
from .soft_delete_filter import pause_listener


class BaseRepository:
    entity: DeclarativeMeta = None

    def __init__(self, entity: DeclarativeMeta):
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
            if key == 'where':
                query = query.where(*options_dict['where'])
            elif key == 'order_by':
                query = query.order_by(*options_dict['order_by'])
            elif key == 'skip':
                query = query.offset(options_dict['skip'])
            elif key == 'take':
                query = query.limit(options_dict['take'])
            elif key == 'relations':
                query = query.options(lazyload(*options_dict['relations']))  # TODO: Not tested yet
            elif key == 'with_deleted':
                self.with_deleted = options_dict['with_deleted']
            else:
                raise InternalServerError(f'Unknown option: {key} in FindOptions')

        return query

    @classmethod
    def __fix_options_dict(
            cls, options_dict: Union[FindManyOptions, FindOneOptions]
    ) -> Union[FindManyOptions, FindOneOptions]:
        for attribute in ['where', 'order_by', 'options']:
            if attribute in options_dict and not isinstance(options_dict[attribute], list):
                options_dict[attribute] = [options_dict[attribute]]

        return options_dict

    def __generate_find_one_options_dict(self, criteria: Union[str, int]) -> FindOneOptions:
        return {
            'where': [inspect(self.entity).primary_key[0] == criteria]
        }

    # ----------- PUBLIC METHODS -----------
    async def find(self, db: Session, options_dict: FindManyOptions = None) -> Optional[List[type(entity)]]:
        query = db.query(self.entity)

        query = self.__apply_options(query, options_dict)
        with pause_listener.pause(self.with_deleted):
            self.with_deleted = False
            return query.all()

    async def find_and_count(
            self, db: Session, options_dict: FindManyOptions = None
    ) -> Optional[Tuple[List[type(entity)], int]]:
        query = db.query(self.entity)

        query = self.__apply_options(query, options_dict)
        with pause_listener.pause(self.with_deleted):
            self.with_deleted = False
            count = query.offset(None).limit(None).count()
            return query.all(), count

    async def find_one(self, db: Session, criteria: Union[str, int, FindOneOptions]) -> Optional[type(entity)]:
        query = db.query(self.entity)

        if isinstance(criteria, (str, int)):
            criteria = self.__generate_find_one_options_dict(criteria)
        query = self.__apply_options(query, criteria)

        try:
            with pause_listener.pause(self.with_deleted):
                self.with_deleted = False
                return query.first()
        except Exception:
            return None

    async def find_one_or_fail(self, db: Session, criteria: Union[str, int, FindOneOptions]) -> Optional[type(entity)]:
        result = await self.find_one(db, criteria)

        if not result:
            message = f'Could not find any entity of type "{self.entity.__name__}" that matches the criteria'
            raise NotFoundException(message, [self.entity.__name__, str(criteria)])     # TODO: Resolver criteria

        return result

    async def create(self, db: Session, _entity: Union[type(entity), BaseModel]) -> type(entity):
        if isinstance(_entity, BaseModel):
            partial_data_entity = _entity.dict(exclude_unset=True)
            _entity = self.entity(**partial_data_entity)

        db.add(_entity)
        return _entity

    async def save(self, db: Session, _entity: type(entity)) -> Optional[type(entity)]:
        db.commit()
        db.refresh(_entity)
        return _entity

    async def delete(self, db: Session, criteria: Union[str, int, FindOneOptions]) -> Optional[DeleteResult]:
        entity = await self.find_one_or_fail(db, criteria)

        db.delete(entity)
        db.commit()

        return DeleteResult(raw=[], affected=1)

    async def soft_delete(self, db: Session, criteria: Union[str, int, FindOneOptions]) -> Optional[UpdateResult]:
        entity = await self.find_one_or_fail(db, criteria)
        columns = get_columns(self.entity)

        for column in columns:
            if 'delete_column' in column.info:
                setattr(entity, column.name, datetime.now())
                db.commit()
                return UpdateResult(raw=[], affected=1, generatedMaps=[])

        raise InternalServerError('Could not find any column with "delete_column" metadata')

    async def update(
            self, db: Session, criteria: Union[str, int, FindOneOptions], partial_entity: Union[BaseModel, dict]
    ) -> Optional[UpdateResult]:
        entity = await self.find_one_or_fail(db, criteria)

        if isinstance(partial_entity, BaseModel):
            partial_entity = partial_entity.dict(exclude_unset=True)
        for key, value in partial_entity.items():
            setattr(entity, key, value)

        db.commit()
        return UpdateResult(raw=[], affected=1, generatedMaps=[])
