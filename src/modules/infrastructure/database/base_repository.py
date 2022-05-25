from typing import Any, List, Optional, Tuple, Union

from sqlalchemy.inspection import inspect
from sqlalchemy.orm import DeclarativeMeta, lazyload, Query, Session
from sqlalchemy.sql.elements import and_

from src.core.types.delete_result_type import DeleteResult
from src.core.types.exceptions_type import InternalServerError, NotFoundException
from src.core.types.find_many_options_type import FindManyOptions
from src.core.types.find_one_options_type import FindOneOptions


class BaseRepository:
    entity: DeclarativeMeta = None

    def __init__(self, entity: DeclarativeMeta):
        self.entity = entity

    # ----------- PRIVATE METHODS -----------
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

    def __generate_find_one_options_dict(self, criteria: Union[str, int]) -> FindOneOptions:
        return {
            'where': [inspect(self.entity).primary_key[0] == criteria]
        }

    # ----------- PUBLIC METHODS -----------
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

    def find_one(self, db: Session, criteria: Union[str, int, FindOneOptions]) -> Optional[type(entity)]:
        query = db.query(self.entity)

        if isinstance(criteria, str) or isinstance(criteria, int):
            criteria = self.__generate_find_one_options_dict(criteria)
        query = self.__apply_options(query, criteria)

        try:
            return query.first()
        except Exception:
            return None

    def find_one_or_fail(self, db: Session, criteria: Union[str, int, FindOneOptions]) -> Optional[type(entity)]:
        result = self.find_one(db, criteria)

        if result is None:
            message = f'Could not find any entity of type "{self.entity.__name__}" matching: '
            if type(criteria) is FindOneOptions or type(criteria) is dict:
                message += f'"{[clause.right.value for clause in criteria["where"]]}"'
            else:
                message += f'"{criteria}"'
            raise NotFoundException(message)

        return result

    def create(self, db: Session, _entity: type(entity)) -> type(entity):
        db.add(_entity)
        return _entity

    def save(self, db: Session, _entity: type(entity)) -> Optional[type(entity)]:
        db.commit()
        db.refresh(_entity)
        return _entity

    def delete(self, db: Session, criteria: Union[str, int, FindOneOptions]) -> Optional[DeleteResult]:
        entity = self.find_one_or_fail(db, criteria)

        db.delete(entity)
        db.commit()

        return DeleteResult(raw=[], affected=1)
