from typing import Any, List, Optional, Tuple, Union

from sqlalchemy.inspection import inspect
from sqlalchemy.orm import DeclarativeMeta, lazyload, Query, Session
from sqlalchemy.sql.elements import and_

from src.core.types.exceptions_type import InternalServerError, NotFoundException
from src.core.types.find_many_options_type import FindManyOptions
from src.core.types.find_one_options_type import FindOneOptions


class BaseRepository:
    entity: DeclarativeMeta = None

    def __init__(self, entity: DeclarativeMeta):
        self.entity = entity

    @classmethod
    def __apply_options(
            cls, query: Query, options_dict: Union[FindManyOptions, FindManyOptions] = None
    ) -> Query:
        if options_dict is None:
            return query

        options_dict = cls.__fix_options_dict(options_dict)

        for key in options_dict.keys():
            if key == 'where':
                query = query.where((and_(*options_dict['where'])))
            elif key == 'order_by':
                query = query.order_by(*options_dict['order_by'])
            elif key == 'skip':
                query = query.offset(options_dict['skip'])
            elif key == 'take':
                query = query.limit(options_dict['take'])
            elif key == 'relations':
                query = query.options(lazyload(*options_dict['relations']))  # TODO: Not tested yet
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

    def __generate_find_one_options_dict(
            self, id: Union[str, int], options_dict: Union[FindOneOptions, None]
    ) -> FindOneOptions:
        if options_dict is None:
            options_dict = {}

        if id is not None:
            self.__fix_options_dict(options_dict)

            if 'where' not in options_dict:
                options_dict['where'] = []

            options_dict['where'] += [inspect(self.entity).primary_key[0] == id]

        return options_dict

    def find(self, db: Session, options_dict: FindManyOptions = None) -> Optional[List[type(entity)]]:
        query = db.query(self.entity)

        query = self.__apply_options(query, options_dict)
        return query.all()

    def find_and_count(
            self, db: Session, options_dict: FindManyOptions = None
    ) -> Optional[Tuple[List[type(entity)], int]]:
        query = db.query(self.entity)

        count = self.__apply_options(query).count()
        query = self.__apply_options(query, options_dict)
        return query.all(), count

    def find_one(
            self, db: Session, id: Union[str, int] = None, options_dict: FindOneOptions = None
    ) -> Optional[type(entity)]:
        query = db.query(self.entity)

        if id is not None:
            options_dict = self.__generate_find_one_options_dict(id, options_dict)
        query = self.__apply_options(query, options_dict)
        try:
            return query.first()
        except Exception as e:
            return None

    def find_one_or_fail(
            self, db: Session, id: Union[str, int] = None, options_dict: FindOneOptions = None
    ) -> Optional[type(entity)]:
        result = self.find_one(db, id, options_dict)

        if result is None:
            message = f'Could not find any entity of type "{self.entity.__name__}" matching: '
            if options_dict is not None:
                raise NotFoundException(
                    message + f'"{[clause.right.value for clause in options_dict["where"]]}"'
                )
            else:
                raise NotFoundException(message + f'"{id}"')

        return result

    def create(self, db: Session, _entity: type(entity)) -> type(entity):
        db.add(_entity)
        return _entity

    def save(self, db: Session, _entity: type(entity)) -> Optional[type(entity)]:
        db.commit()
        db.refresh(_entity)
        return _entity

    def delete(self, db: Session, criteria: Union[str, int, FindOneOptions]) -> Optional[Any]:
        if isinstance(criteria, str) or isinstance(criteria, int):
            entity = self.find_one_or_fail(db, id=criteria)
        else:
            entity = self.find_one_or_fail(db, options_dict=criteria)

        db.delete(entity)
        db.commit()
