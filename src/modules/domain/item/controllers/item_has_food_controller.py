from fastapi import APIRouter

from src.modules.domain.item.services.item_has_food_service import ItemHasFoodService

item_has_food_router = APIRouter(tags=["Item Has Food"], prefix="/item-has-food")

item_has_food_service = ItemHasFoodService()
