from fastapi import APIRouter

from src.modules.domain.diary.services.diary_service import DiaryService

diary_router = APIRouter(tags=["Diary"], prefix="/diary")

diary_service = DiaryService()
