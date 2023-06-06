from typing import Optional

import pytest
from httpx import AsyncClient
from starlette.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_403_FORBIDDEN,
    HTTP_422_UNPROCESSABLE_ENTITY,
)

from src.main import app
from src.modules.domain.recommendation_system.services.recommendation_system_service import (
    RecommendationSystemService,
)
from src.modules.infrastructure.auth.dto.login_payload_dto import LoginPayloadDto
from test.test_base_e2e import TestBaseE2E

CONTROLLER = "recommendation-system"
rm_service = RecommendationSystemService()


@pytest.mark.describe(f"POST Route: /{CONTROLLER}/complete-nutritional-plan")
class TestCompleteUserNutritionalPlan(TestBaseE2E):
    route = f"/{CONTROLLER}/complete-nutritional-plan"

    @pytest.mark.asyncio
    @pytest.mark.it("Success: Complete User's Nutritional Plan")
    async def test_complete_nutritional_plan(self, user_admin: Optional[LoginPayloadDto]) -> None:
        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            response = await ac.post(
                self.route,
                params={
                    "user_id": "3e535e14-d26c-4dc8-ae28-096ff05453fb",
                    "nutritional_plan_id": "9d64aec5-3ddb-4d5f-a824-341f0a4928f1",
                },
                headers={"Authorization": f"Bearer {user_admin.access_token}"},
            )

        data = response.json()

        assert response.status_code == HTTP_200_OK
        assert isinstance(data, list)
        assert len(data) >= 2
        assert all(key in data[0] for key in ["id", "description", "score"])
        assert data[0]["score"] >= data[-1]["score"]

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Complete Nutritional Plan without any type of meal")
    async def test_any_type_of_meal(self, user_admin: Optional[LoginPayloadDto]) -> None:
        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            assert (
                await ac.post(
                    self.route,
                    params={
                        "user_id": "3e535e14-d26c-4dc8-ae28-096ff05453fb",
                        "nutritional_plan_id": "ba325e6c-1b2b-49ad-a1d1-4883cd338865",
                    },
                    headers={"Authorization": f"Bearer {user_admin.access_token}"},
                )
            ).status_code == HTTP_400_BAD_REQUEST

    @pytest.mark.asyncio
    @pytest.mark.it("Failure:  Complete Nutritional Plan without required fields")
    async def test_complete_nutritional_plan_without_required_field(
        self, user_admin: Optional[LoginPayloadDto]
    ) -> None:
        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            response = await ac.post(
                self.route,
                headers={"Authorization": f"Bearer {user_admin.access_token}"},
            )

        data = response.json()

        assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY
        assert data["detail"][0]["msg"] == "field required"
        assert data["detail"][0]["loc"] == ["query", "user_id"]

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Complete Nutritional Plan without required authorization")
    async def test_complete_nutritional_plan_without_required_authorization(
        self, user_common: Optional[LoginPayloadDto]
    ) -> None:
        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            assert (
                await ac.post(
                    self.route,
                    params={
                        "user_id": "3e535e14-d26c-4dc8-ae28-096ff05453fb",
                        "nutritional_plan_id": "9d64aec5-3ddb-4d5f-a824-341f0a4928f1",
                    },
                    headers={"Authorization": f"Bearer {user_common.access_token}"},
                )
            ).status_code == HTTP_403_FORBIDDEN


@pytest.mark.describe(f"GET Route: /{CONTROLLER}/food-preferences")
class TestGetUserFoodPreferences(TestBaseE2E):
    route = f"/{CONTROLLER}/food-preferences"

    @pytest.mark.asyncio
    @pytest.mark.it("Success: Get a list of all user's food preferences")
    async def test_get_user_food_preferences(self, user_admin: Optional[LoginPayloadDto]) -> None:
        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            response = await ac.get(
                self.route,
                headers={"Authorization": f"Bearer {user_admin.access_token}"},
                params={
                    "user_id": "3e535e14-d26c-4dc8-ae28-096ff05453fb",
                    "nutritional_plan_id": "9d64aec5-3ddb-4d5f-a824-341f0a4928f1",
                },
            )

        body = response.json()

        assert response.status_code == HTTP_200_OK
        assert isinstance(body, list)
        assert len(body) >= 2

        for food in body:
            if food["id"] == "950d760f-ba5c-44ca-b4ec-313510e59beb":
                assert food["score"] == 25

            if food["id"] == "e3ff57d6-eb77-48de-bb49-ff9201d95926":
                assert food["score"] == -25

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Get a list of all user's food preferences without authentication")
    async def test_no_authentication(self) -> None:
        await self.get_no_authentication(self.route)

    @pytest.mark.asyncio
    @pytest.mark.it(
        "Failure: Get a list of all user's food preferences with non required authentication"
    )
    async def test_different_required_authentication(
        self, user_common: Optional[LoginPayloadDto]
    ) -> None:
        await self.get_different_required_authentication(self.route, user_common)
