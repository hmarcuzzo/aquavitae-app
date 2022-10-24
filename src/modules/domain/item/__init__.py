from fastapi import APIRouter

from .entities.item_entity import Item
from .controllers.item_controller import item_router

from .entities.item_has_food import ItemHasFood
from .controllers.item_has_food_controller import item_has_food_router

item_routers = APIRouter()
item_routers.include_router(item_router)
item_routers.include_router(item_has_food_router)

item_entities = [Item, ItemHasFood]
