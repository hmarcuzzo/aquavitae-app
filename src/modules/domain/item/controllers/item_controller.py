from fastapi import APIRouter

from src.modules.domain.item.services.item_service import ItemService

item_router = APIRouter(tags=["Item"], prefix="/item")

item_service = ItemService()
