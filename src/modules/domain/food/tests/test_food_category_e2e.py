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

from src.main import app
from src.modules.domain.food.entities.food_category_entity import FoodCategory
from src.modules.domain.food.entities.food_entity import Food
from src.modules.domain.food.repositories.food_repository import FoodRepository
from src.modules.domain.food.services.food_category_service import FoodCategoryService
from src.modules.infrastructure.auth.dto.login_payload_dto import LoginPayloadDto
from test.test_base_e2e import TestBaseE2E

CONTROLLER = "food-category"
food_category_service = FoodCategoryService()


@pytest.mark.describe(f"POST Route: /{CONTROLLER}/create")
class TestCreateFoodCategory(TestBaseE2E):
    route = f"/{CONTROLLER}/create"

    @pytest.mark.asyncio
    @pytest.mark.it("Success: Create a food category")
    async def test_create_new_food_category(self, user_admin: Optional[LoginPayloadDto]) -> None:
        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            response = await ac.post(
                self.route,
                json={
                    "description": "Level 9",
                    "level": 9,
                    "food_category": "42853fe7-5bf7-4503-af2c-2b284b5fdfbe",
                },
                headers={"Authorization": f"Bearer {user_admin.access_token}"},
            )

        data = response.json()

        assert response.status_code == HTTP_201_CREATED
        assert [hasattr(data, attr_name) for attr_name in ["id", "description", "level"]]
        assert data["description"] == "Level 9"
        assert data["level"] == 9

        activity_level_dto = await food_category_service.find_one_food_category(
            data["id"], self.db_test_utils.db
        )

        assert activity_level_dto is not None
        assert activity_level_dto.description == data["description"]

    @pytest.mark.asyncio
    @pytest.mark.it("Success: Create a food category without relationship")
    async def test_create_new_food_category_no_relationship(
        self, user_admin: Optional[LoginPayloadDto]
    ) -> None:
        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            response = await ac.post(
                self.route,
                json={
                    "description": "Level 40",
                    "level": 40,
                },
                headers={"Authorization": f"Bearer {user_admin.access_token}"},
            )

        data = response.json()

        assert response.status_code == HTTP_201_CREATED
        assert data["food_category"] is None

        activity_level_dto = await food_category_service.find_one_food_category(
            data["id"], self.db_test_utils.db
        )

        assert activity_level_dto is not None
        assert activity_level_dto.food_category is None

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Create a food category with deleted relation")
    async def test_create_food_category_with_deleted_relation(
        self, user_admin: Optional[LoginPayloadDto]
    ) -> None:
        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            assert (
                await ac.post(
                    self.route,
                    json={
                        "description": "Level 77",
                        "level": 77,
                        "food_category": "4f6541f4-5558-4c0d-9d65-870a6549f2e0",
                    },
                    headers={"Authorization": f"Bearer {user_admin.access_token}"},
                )
            ).status_code == HTTP_404_NOT_FOUND

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Create a food category without required fields")
    async def test_create_food_category_without_required_field(
        self, user_admin: Optional[LoginPayloadDto]
    ) -> None:
        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            response = await ac.post(
                self.route,
                json={
                    "description": "Level 9",
                    "food_category": "42853fe7-5bf7-4503-af2c-2b284b5fdfbe",
                },
                headers={"Authorization": f"Bearer {user_admin.access_token}"},
            )

        data = response.json()

        assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY
        assert data["detail"][0]["msg"] == "field required"
        assert data["detail"][0]["loc"] == ["body", "level"]

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Create a food category without required authorization")
    async def test_create_food_category_without_required_authorization(
        self, user_common: Optional[LoginPayloadDto], user_nutritionist: Optional[LoginPayloadDto]
    ) -> None:
        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            assert (
                await ac.post(
                    self.route,
                    json={
                        "description": "Level 99",
                        "level": 99,
                    },
                    headers={"Authorization": f"Bearer {user_common.access_token}"},
                )
            ).status_code == HTTP_403_FORBIDDEN


@pytest.mark.describe(f"GET Route: /{CONTROLLER}/get")
class TestGetAllFoodCategories(TestBaseE2E):
    route = f"/{CONTROLLER}/get"

    @pytest.mark.asyncio
    @pytest.mark.it("Success: Get a list of all food category")
    async def test_get_food_categories(self, user_admin: Optional[LoginPayloadDto]) -> None:
        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            response = await ac.get(
                self.route,
                headers={"Authorization": f"Bearer {user_admin.access_token}"},
                params={"columns": ["food_category"]},
            )

        body = response.json()
        data = body["data"]

        assert response.status_code == HTTP_200_OK
        assert body["count"] >= 0

        for food_category in data:
            if food_category["id"] == "75827c83-d4cb-46cb-a092-9ba2dd962023":
                assert food_category["description"] == "Level 2"
                assert food_category["level"] == 2
                assert food_category["food_category"] is None

            if food_category["id"] == "90e719b0-0f32-4236-82e7-033e2deae8fd":
                assert food_category["description"] == "Level 3"
                assert food_category["level"] == 3
                assert (
                    food_category["food_category"]["id"] == "75827c83-d4cb-46cb-a092-9ba2dd962023"
                )
                assert food_category["food_category"]["food_category"] is None

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Get a list of all food categories without authentication")
    async def test_no_authentication(self) -> None:
        await self.get_no_authentication(self.route)

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Get a list of all food categories with non required authentication")
    @pytest.mark.parametrize("user", ["user_common"])
    async def test_different_required_authentication(
        self, user: str, request: FixtureRequest
    ) -> None:
        user: LoginPayloadDto = request.getfixturevalue(user)
        await self.get_different_required_authentication(self.route, user)


@pytest.mark.describe(f"GET Route: /{CONTROLLER}/get/<id>")
class TestGetFoodCategoryById(TestBaseE2E):
    route = f"/{CONTROLLER}/get/"

    @pytest.mark.asyncio
    @pytest.mark.it("Success: Get one food category by id")
    async def test_get_food_category_by_id(self, user_admin: Optional[LoginPayloadDto]) -> None:
        food_category_item = self.db_test_utils.get_entity_objects(FoodCategory)[2]

        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            response = await ac.get(
                self.route + f"{food_category_item['id']}",
                headers={"Authorization": f"Bearer {user_admin.access_token}"},
            )

        data: dict = response.json()

        assert response.status_code == HTTP_200_OK
        assert isinstance(data, dict)
        assert data["id"] == food_category_item["id"]
        assert data["description"] == food_category_item["description"]
        assert data["level"] == food_category_item["level"]
        assert data["food_category"] is None

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Get one food category without authentication")
    async def test_no_authentication(self) -> None:
        await self.get_no_authentication(self.route)

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Get one food category with non required authentication")
    @pytest.mark.parametrize("user", ["user_common"])
    async def test_different_required_authentication(
        self, user: str, request: FixtureRequest
    ) -> None:
        user: LoginPayloadDto = request.getfixturevalue(user)
        await self.get_different_required_authentication(self.route, user)


@pytest.mark.describe(f"DELETE Route: /{CONTROLLER}/delete/<id>")
class TestDeleteFoodCategory(TestBaseE2E):
    route = f"/{CONTROLLER}/delete"

    @pytest.mark.asyncio
    @pytest.mark.it("Success: Delete food category")
    async def test_delete_food_category(self, user_admin: Optional[LoginPayloadDto]) -> None:
        food_category_item = self.db_test_utils.get_entity_objects(FoodCategory)[2]

        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            response = await ac.delete(
                f"{self.route}/{food_category_item['id']}",
                headers={"Authorization": f"Bearer {user_admin.access_token}"},
            )

        assert response.status_code == HTTP_200_OK

        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            response = await ac.get(
                f"/{CONTROLLER}/get/{food_category_item['id']}",
                headers={"Authorization": f"Bearer {user_admin.access_token}"},
            )

        assert response.status_code == HTTP_404_NOT_FOUND

    @pytest.mark.asyncio
    @pytest.mark.it("Success: Check if all relation from food category, was deleted")
    async def test_delete_food_category_relations(
        self, user_admin: Optional[LoginPayloadDto], user_common: Optional[LoginPayloadDto]
    ) -> None:
        food_category_item = self.db_test_utils.get_entity_objects(FoodCategory)[2]

        food_repository = FoodRepository()
        response = await food_repository.find(
            {
                "where": Food.food_category_id == food_category_item["id"],
                "relations": ["food_category"],
            },
            self.db_test_utils.db,
        )

        assert isinstance(response, list)
        assert len(response) == 0

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Delete food category already deleted")
    async def test_delete_food_category_already_deleted(
        self, user_admin: Optional[LoginPayloadDto]
    ) -> None:
        food_category_item = self.db_test_utils.get_entity_objects(FoodCategory)[1]

        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            assert (
                await ac.delete(
                    f"{self.route}/{food_category_item['id']}",
                    headers={"Authorization": f"Bearer {user_admin.access_token}"},
                )
            ).status_code == HTTP_404_NOT_FOUND

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Delete food category without authentication")
    async def test_no_authentication(self) -> None:
        food_category_item = self.db_test_utils.get_entity_objects(FoodCategory)[2]
        await self.del_no_authentication(f"{self.route}/{food_category_item['id']}")

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Delete food category without required authentication")
    @pytest.mark.parametrize("user", ["user_common"])
    async def test_different_required_authentication(
        self, user: str, request: FixtureRequest
    ) -> None:
        food_category_item = self.db_test_utils.get_entity_objects(FoodCategory)[2]
        user: LoginPayloadDto = request.getfixturevalue(user)
        await self.del_different_required_authentication(
            f"{self.route}/{food_category_item['id']}", user
        )


@pytest.mark.describe(f"PATCH Route: /{CONTROLLER}/update/<id>")
class TestUpdateFoodCategory(TestBaseE2E):
    route = f"/{CONTROLLER}/update"

    @pytest.mark.asyncio
    @pytest.mark.it("Success: Update food category")
    async def test_update_food_category(self, user_admin: Optional[LoginPayloadDto]) -> None:
        food_category_item = self.db_test_utils.get_entity_objects(FoodCategory)[0]

        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            response = await ac.patch(
                f"{self.route}/{food_category_item['id']}",
                json={"description": "Level 0"},
                headers={"Authorization": f"Bearer {user_admin.access_token}"},
            )

        assert response.status_code == HTTP_200_OK

        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            response = await ac.get(
                f"/{CONTROLLER}/get/{food_category_item['id']}",
                headers={"Authorization": f"Bearer {user_admin.access_token}"},
            )

        data = response.json()

        assert response.status_code == HTTP_200_OK
        assert data["description"] == "Level 0"

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Update food category without authentication")
    async def test_no_authentication(self) -> None:
        food_category_item = self.db_test_utils.get_entity_objects(FoodCategory)[0]
        await self.patch_no_authentication(f"{self.route}/{food_category_item['id']}")

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Update food category without required authentication")
    @pytest.mark.parametrize("user", ["user_common"])
    async def test_different_required_authentication(
        self, user: str, request: FixtureRequest
    ) -> None:
        food_category_item = self.db_test_utils.get_entity_objects(FoodCategory)[0]
        user: LoginPayloadDto = request.getfixturevalue(user)
        await self.patch_different_required_authentication(
            f"{self.route}/{food_category_item['id']}", user
        )
