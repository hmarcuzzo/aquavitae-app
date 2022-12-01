from typing import Optional

import pytest
from _pytest.fixtures import FixtureRequest
from httpx import AsyncClient
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_422_UNPROCESSABLE_ENTITY,
)

from src.core.types.exceptions_type import NotFoundException
from src.main import app
from src.modules.domain.food.entities.food_category_entity import FoodCategory
from src.modules.domain.food.entities.food_entity import Food
from src.modules.domain.food.repositories.food_repository import FoodRepository
from src.modules.domain.food.services.food_category_service import FoodCategoryService
from src.modules.domain.food.services.food_service import FoodService
from src.modules.infrastructure.auth.dto.login_payload_dto import LoginPayloadDto
from test.test_base_e2e import TestBaseE2E

CONTROLLER = "food"
food_service = FoodService()


@pytest.mark.describe(f"POST Route: /{CONTROLLER}/create")
class TestCreateFood(TestBaseE2E):
    route = f"/{CONTROLLER}/create"

    @pytest.mark.asyncio
    @pytest.mark.it("Success: Create a food")
    async def test_create_new_food(self, user_admin: Optional[LoginPayloadDto]) -> None:
        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            response = await ac.post(
                self.route,
                json={
                    "description": "Food Test 1",
                    "proteins": 0,
                    "lipids": 0,
                    "carbohydrates": 0,
                    "energy_value": 95,
                    "potassium": 0,
                    "phosphorus": 0,
                    "sodium": 0,
                    "food_category": "42853fe7-5bf7-4503-af2c-2b284b5fdfbe",
                },
                headers={"Authorization": f"Bearer {user_admin.access_token}"},
            )

        data = response.json()

        assert response.status_code == HTTP_201_CREATED
        assert [hasattr(data, attr_name) for attr_name in ["id", "energy_value"]]
        assert data["energy_value"] == 95

        activity_level_dto = await food_service.find_one_food(data["id"], self.db_test_utils.db)

        assert activity_level_dto is not None
        assert activity_level_dto.energy_value == data["energy_value"]

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Create a food with deleted relation")
    async def test_create_food_with_deleted_relation(
        self, user_admin: Optional[LoginPayloadDto]
    ) -> None:
        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            assert (
                await ac.post(
                    self.route,
                    json={
                        "description": "Food Test 2",
                        "proteins": 0,
                        "lipids": 0,
                        "carbohydrates": 0,
                        "energy_value": 92,
                        "potassium": 0,
                        "phosphorus": 0,
                        "sodium": 0,
                        "food_category": "4f6541f4-5558-4c0d-9d65-870a6549f2e0",
                    },
                    headers={"Authorization": f"Bearer {user_admin.access_token}"},
                )
            ).status_code == HTTP_404_NOT_FOUND

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Create a food without required fields")
    async def test_create_food_without_required_field(
        self, user_admin: Optional[LoginPayloadDto]
    ) -> None:
        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            response = await ac.post(
                self.route,
                json={
                    "description": "Food Test 3",
                    "proteins": 0,
                    "lipids": 0,
                    "carbohydrates": 0,
                    "energy_value": 93,
                    "potassium": 0,
                    "phosphorus": 0,
                    "food_category": "42853fe7-5bf7-4503-af2c-2b284b5fdfbe",
                },
                headers={"Authorization": f"Bearer {user_admin.access_token}"},
            )

        data = response.json()

        assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY
        assert data["detail"][0]["msg"] == "field required"
        assert data["detail"][0]["loc"] == ["body", "sodium"]

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Create a food without required authorization")
    async def test_create_food_without_required_authorization(
        self, user_common: Optional[LoginPayloadDto], user_nutritionist: Optional[LoginPayloadDto]
    ) -> None:
        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            assert (
                await ac.post(
                    self.route,
                    json={
                        "description": "Food Test 6",
                        "proteins": 0,
                        "lipids": 0,
                        "carbohydrates": 0,
                        "energy_value": 96,
                        "potassium": 0,
                        "phosphorus": 0,
                        "sodium": 0,
                        "food_category": "42853fe7-5bf7-4503-af2c-2b284b5fdfbe",
                    },
                    headers={"Authorization": f"Bearer {user_common.access_token}"},
                )
            ).status_code == HTTP_403_FORBIDDEN


@pytest.mark.describe(f"GET Route: /{CONTROLLER}/get")
class TestGetAllFoods(TestBaseE2E):
    route = f"/{CONTROLLER}/get"

    @pytest.mark.asyncio
    @pytest.mark.it("Success: Get a list of all food")
    async def test_get_foods(self, user_admin: Optional[LoginPayloadDto]) -> None:
        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            response = await ac.get(
                self.route,
                headers={"Authorization": f"Bearer {user_admin.access_token}"},
                params={"columns": ["description", "food_category"]},
            )

        body = response.json()
        data = body["data"]

        assert response.status_code == HTTP_200_OK
        assert body["count"] >= 0

        for food_category in data:
            if food_category["id"] == "950d760f-ba5c-44ca-b4ec-313510e59beb":
                assert food_category["description"] == "Food 1"
                assert (
                    food_category["food_category"]["id"] == "75827c83-d4cb-46cb-a092-9ba2dd962023"
                )
                assert food_category["food_category"]["food_category"] is None

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Get a list of all food without authentication")
    async def test_no_authentication(self) -> None:
        await self.get_no_authentication(self.route)

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Get a list of all food with non required authentication")
    @pytest.mark.parametrize("user", ["user_common"])
    async def test_different_required_authentication(
        self, user: str, request: FixtureRequest
    ) -> None:
        user: LoginPayloadDto = request.getfixturevalue(user)
        await self.get_different_required_authentication(self.route, user)


@pytest.mark.describe(f"GET Route: /{CONTROLLER}/get/<id>")
class TestGetFoodById(TestBaseE2E):
    route = f"/{CONTROLLER}/get/"

    @pytest.mark.asyncio
    @pytest.mark.it("Success: Get one food by id")
    async def test_get_food_by_id(self, user_admin: Optional[LoginPayloadDto]) -> None:
        food_item = self.db_test_utils.get_entity_objects(Food)[0]

        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            response = await ac.get(
                self.route + f"{food_item['id']}",
                headers={"Authorization": f"Bearer {user_admin.access_token}"},
            )

        data: dict = response.json()

        assert response.status_code == HTTP_200_OK
        assert isinstance(data, dict)
        assert data["id"] == food_item["id"]
        assert data["description"] == food_item["description"]
        assert data["food_category"]["id"] == food_item["food_category_id"]

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Get one food without authentication")
    async def test_no_authentication(self) -> None:
        await self.get_no_authentication(self.route)

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Get one food with non required authentication")
    @pytest.mark.parametrize("user", ["user_common"])
    async def test_different_required_authentication(
        self, user: str, request: FixtureRequest
    ) -> None:
        user: LoginPayloadDto = request.getfixturevalue(user)
        await self.get_different_required_authentication(self.route, user)


@pytest.mark.describe(f"DELETE Route: /{CONTROLLER}/delete/<id>")
class TestDeleteFood(TestBaseE2E):
    route = f"/{CONTROLLER}/delete"

    @pytest.mark.asyncio
    @pytest.mark.it("Success: Delete food")
    async def test_delete_food(self, user_admin: Optional[LoginPayloadDto]) -> None:
        food_item = self.db_test_utils.get_entity_objects(Food)[0]

        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            response = await ac.delete(
                f"{self.route}/{food_item['id']}",
                headers={"Authorization": f"Bearer {user_admin.access_token}"},
            )

        assert response.status_code == HTTP_200_OK

        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            response = await ac.get(
                f"/{CONTROLLER}/get/{food_item['id']}",
                headers={"Authorization": f"Bearer {user_admin.access_token}"},
            )

        assert response.status_code == HTTP_404_NOT_FOUND

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Delete food already deleted")
    async def test_delete_food_category_already_deleted(
        self, user_admin: Optional[LoginPayloadDto]
    ) -> None:
        food_item = self.db_test_utils.get_entity_objects(Food)[0]

        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            assert (
                await ac.delete(
                    f"{self.route}/{food_item['id']}",
                    headers={"Authorization": f"Bearer {user_admin.access_token}"},
                )
            ).status_code == HTTP_404_NOT_FOUND

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Delete food without authentication")
    async def test_no_authentication(self) -> None:
        food_item = self.db_test_utils.get_entity_objects(Food)[1]
        await self.del_no_authentication(f"{self.route}/{food_item['id']}")

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Delete food without required authentication")
    @pytest.mark.parametrize("user", ["user_common"])
    async def test_different_required_authentication(
        self, user: str, request: FixtureRequest
    ) -> None:
        food_item = self.db_test_utils.get_entity_objects(Food)[1]
        user: LoginPayloadDto = request.getfixturevalue(user)
        await self.del_different_required_authentication(f"{self.route}/{food_item['id']}", user)


@pytest.mark.describe(f"PATCH Route: /{CONTROLLER}/update/<id>")
class TestUpdateFood(TestBaseE2E):
    route = f"/{CONTROLLER}/update"

    @pytest.mark.asyncio
    @pytest.mark.it("Success: Update food")
    async def test_update_food(self, user_admin: Optional[LoginPayloadDto]) -> None:
        food_item = self.db_test_utils.get_entity_objects(Food)[1]

        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            assert (
                await ac.patch(
                    f"{self.route}/{food_item['id']}",
                    json={"description": "Food 2 updated"},
                    headers={"Authorization": f"Bearer {user_admin.access_token}"},
                )
            ).status_code == HTTP_200_OK

        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            response = await ac.get(
                f"/{CONTROLLER}/get/{food_item['id']}",
                headers={"Authorization": f"Bearer {user_admin.access_token}"},
            )

        data = response.json()

        assert response.status_code == HTTP_200_OK
        assert data["description"] == "Food 2 updated"

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Update food without authentication")
    async def test_no_authentication(self) -> None:
        food_item = self.db_test_utils.get_entity_objects(Food)[1]
        await self.patch_no_authentication(f"{self.route}/{food_item['id']}")

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Update food without required authentication")
    @pytest.mark.parametrize("user", ["user_common"])
    async def test_different_required_authentication(
        self, user: str, request: FixtureRequest
    ) -> None:
        food_item = self.db_test_utils.get_entity_objects(Food)[1]
        user: LoginPayloadDto = request.getfixturevalue(user)
        await self.patch_different_required_authentication(f"{self.route}/{food_item['id']}", user)
