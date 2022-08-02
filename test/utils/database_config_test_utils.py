import json
import os
from typing import List, TypeVar

from sqlalchemy import inspect, Table
from sqlalchemy.orm import DeclarativeMeta

from config import APP_ENV
from src.modules.infrastructure.database import get_db
from src.modules.infrastructure.database.base import Base
from src.modules.infrastructure.database.session import engine

T = TypeVar("T")


class DatabaseConfigTest:
    def __init__(self):
        if APP_ENV != "test":
            raise Exception("This class is only for testing purposes")
        self.db = next(get_db())

    # ----------- PRIVATE METHODS -----------
    @staticmethod
    def __get_fixture_file(entity: Table) -> str:
        return os.path.join(
            os.path.dirname(os.path.realpath(__file__)), f"../fixtures/{entity.name}.json"
        )

    def __get_items_from_fixture(self, entity: Table) -> List[dict]:
        fixture_file = self.__get_fixture_file(entity)
        items = []
        if os.path.exists(fixture_file):
            items = json.load(open(fixture_file, encoding="utf-8"))

        return items

    # ----------- PUBLIC METHODS -----------
    async def close_db_connection(self) -> None:
        self.db.close()

    def get_entity_objects(self, entity: T) -> List[dict]:
        entity_table = inspect(entity).local_table
        return self.__get_items_from_fixture(entity_table)

    @staticmethod
    def get_entities() -> List[Table]:
        return Base.metadata.sorted_tables

    async def reload_fixtures(self, entities_input: List[DeclarativeMeta] = None) -> None:
        entities = self.get_entities()

        if entities_input:
            apply_entities = []
            for entity_input in entities_input:
                filtered_entity = list(
                    filter(lambda entity: entity.name == entity_input.__tablename__, entities)
                )
                if not filtered_entity.__len__():
                    raise Exception(f"Entity {entity_input.__name__} not found")
                else:
                    apply_entities.append(filtered_entity[0])
            entities = apply_entities

        await self.clean_all(list(reversed(entities)))
        await self.load_all(entities)

    @staticmethod
    async def clean_all(entities: List[Table]) -> None:
        try:
            for entity in entities:
                engine.execute(entity.delete())
        except Exception as e:
            raise Exception(f"Error cleaning test database: {e}")

    async def load_all(self, entities: List[Table]) -> None:
        try:
            for entity in entities:
                items = self.__get_items_from_fixture(entity)
                if items.__len__() > 0:
                    engine.execute(entity.insert(values=items))
        except Exception as e:
            raise Exception(f"Error loading fixtures on test database: {e}")
