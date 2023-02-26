from typing import List, Optional

from cachetools import TTLCache
from sqlalchemy.orm import Session

from src.modules.domain.recommendation_system.dto.user_preferences_table_dto import (
    DetailedUserPreferencesTable,
    SimplifiedUserPreferencesTable,
)
from src.modules.domain.recommendation_system.interfaces.complete_nutritional_plan_interface import (
    CompleteNutritionalPlanInterface,
)
from src.modules.domain.recommendation_system.interfaces.find_user_food_preferences_interface import (
    FindUserFoodPreferencesInterface,
)

all_food_cache = TTLCache(maxsize=1, ttl=60 * 60)
user_food_preference_cache = TTLCache(maxsize=100, ttl=60 * 60)


def all_foods_cache_key(db: Session):
    return f"all_foods_{db.get_bind().url.database}_{db.get_bind().dialect.name}"


class RecommendationSystemService:
    def __init__(self):
        self.find_user_food_preferences_interface = FindUserFoodPreferencesInterface()
        self.complete_nutritional_plan_interface = CompleteNutritionalPlanInterface()

    # ---------------------- PUBLIC METHODS ----------------------
    async def complete_nutritional_plan(
        self,
        user_id: str,
        nutritional_plan_id: str,
        available: bool,
        force_reload: bool,
        db: Session,
    ) -> Optional[List[SimplifiedUserPreferencesTable]]:
        user_items_preference = (
            await self.complete_nutritional_plan_interface.complete_nutritional_plan(
                user_id, nutritional_plan_id, available, force_reload, db
            )
        ).to_dict("records")

        return [SimplifiedUserPreferencesTable(**item) for item in user_items_preference]

    async def get_user_food_preferences(
        self,
        user_id: str,
        nutritional_plan_id: str,
        available: bool,
        force_reload: bool,
        db: Session,
    ) -> Optional[List[DetailedUserPreferencesTable]]:
        return await self.find_user_food_preferences_interface.get_user_food_preferences(
            user_id, nutritional_plan_id, available, force_reload, db
        )
