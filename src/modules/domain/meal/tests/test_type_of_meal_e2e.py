from typing import Optional
from urllib.parse import urljoin

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
from src.modules.domain.meal.entities.type_of_meal_entity import TypeOfMeal
from src.modules.domain.meal.services.type_of_meal_service import TypeOfMealService
from src.modules.infrastructure.auth.dto.login_payload_dto import LoginPayloadDto
from test.test_base_e2e import TestBaseE2E

CONTROLLER = "type-of-meal"
type_of_meal_service = TypeOfMealService()


@pytest.mark.describe(f"POST Route: /{CONTROLLER}/create")
class TestCreateTypeOfMeal(TestBaseE2E):
    route = f"/{CONTROLLER}/create"

    @pytest.mark.asyncio
    @pytest.mark.it("Success: Create a type of meal")
    async def test_create_new_type_of_meal(self, user_admin: Optional[LoginPayloadDto]) -> None:
        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            response = await ac.post(
                self.route,
                json={
                    "description": "Type of Meal Test",
                    "calories_percentage": 60,
                    "lipids_percentage": 55,
                    "proteins_percentage": 30,
                    "carbohydrates_percentage": 15,
                },
                headers={"Authorization": f"Bearer {user_admin.access_token}"},
            )

        data = response.json()

        assert response.status_code == HTTP_201_CREATED
        assert [hasattr(data, attr_name) for attr_name in ["id", "description"]]
        assert data["description"] == "Type of Meal Test"

        type_of_meal_dto = await type_of_meal_service.find_one_type_of_meal(
            data["id"], self.db_test_utils.db
        )

        assert type_of_meal_dto is not None
        assert type_of_meal_dto.description == data["description"]

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Create a type of meal without required fields")
    async def test_create_type_of_meal_without_required_field(
        self, user_admin: Optional[LoginPayloadDto]
    ) -> None:
        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            response = await ac.post(
                self.route,
                json={
                    "description": "Type of Meal Test 2",
                },
                headers={"Authorization": f"Bearer {user_admin.access_token}"},
            )

        data = response.json()

        assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY
        assert data["detail"][0]["msg"] == "field required"
        assert data["detail"][0]["loc"] == ["body", "calories_percentage"]

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Create a type of meal without required authorization")
    async def test_create_type_of_meal_without_required_authorization(
        self, user_common: Optional[LoginPayloadDto], user_nutritionist: Optional[LoginPayloadDto]
    ) -> None:
        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            assert (
                await ac.post(
                    self.route,
                    json={
                        "description": "Type of Meal Test 3",
                        "calories_percentage": 60,
                        "lipids_percentage": 55,
                        "proteins_percentage": 30,
                        "carbohydrates_percentage": 15,
                    },
                    headers={"Authorization": f"Bearer {user_common.access_token}"},
                )
            ).status_code == HTTP_403_FORBIDDEN


@pytest.mark.describe(f"GET Route: /{CONTROLLER}/get")
class TestGetAllTypesOfMeal(TestBaseE2E):
    route = f"/{CONTROLLER}/get"

    @pytest.mark.asyncio
    @pytest.mark.it("Success: Get a list of all type of meal")
    async def test_get_types_of_meal(self, user_admin: Optional[LoginPayloadDto]) -> None:
        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            response = await ac.get(
                self.route,
                headers={"Authorization": f"Bearer {user_admin.access_token}"},
                params={"columns": ["description"]},
            )

        body = response.json()
        data = body["data"]

        assert response.status_code == HTTP_200_OK
        assert body["count"] >= 0

        for type_of_meal in data:
            if type_of_meal["id"] == "e3972574-30bd-4183-9475-b2b9ef477762":
                assert type_of_meal["description"] == "Big Meals"

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Get a list of all types of meal without authentication")
    async def test_no_authentication(self) -> None:
        await self.get_no_authentication(self.route)

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Get a list of all types of meal with non required authentication")
    async def test_different_required_authentication(
        self, user_common: Optional[LoginPayloadDto]
    ) -> None:
        await self.get_different_required_authentication(self.route, user_common)


@pytest.mark.describe(f"GET Route: /{CONTROLLER}/get/<id>")
class TestGetTypeOfMealById(TestBaseE2E):
    route = f"/{CONTROLLER}/get/"

    @pytest.mark.asyncio
    @pytest.mark.it("Success: Get one type of meal by id")
    async def test_get_type_of_meal_by_id(self, user_admin: Optional[LoginPayloadDto]) -> None:
        type_of_meal_item = self.db_test_utils.get_entity_objects(TypeOfMeal)[0]

        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            response = await ac.get(
                self.route + f"{type_of_meal_item['id']}",
                headers={"Authorization": f"Bearer {user_admin.access_token}"},
            )

        data: dict = response.json()

        assert response.status_code == HTTP_200_OK
        assert isinstance(data, dict)
        assert data["id"] == type_of_meal_item["id"]
        assert data["description"] == type_of_meal_item["description"]

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Get one type of meal without authentication")
    async def test_no_authentication(self) -> None:
        type_of_meal_item = self.db_test_utils.get_entity_objects(TypeOfMeal)[0]
        await self.get_no_authentication(self.route + f"{type_of_meal_item['id']}")

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Get one type of meal with non required authentication")
    async def test_different_required_authentication(
        self, user_common: Optional[LoginPayloadDto]
    ) -> None:
        type_of_meal_item = self.db_test_utils.get_entity_objects(TypeOfMeal)[0]
        await self.get_different_required_authentication(
            self.route + f"{type_of_meal_item['id']}", user_common
        )


@pytest.mark.describe(f"DELETE Route: /{CONTROLLER}/delete/<id>")
class TestDeleteTypeOfMeal(TestBaseE2E):
    route = f"/{CONTROLLER}/delete"

    @pytest.mark.asyncio
    @pytest.mark.it("Success: Delete type of meal")
    async def test_delete_type_of_meal(self, user_admin: Optional[LoginPayloadDto]) -> None:
        type_of_meal_item = self.db_test_utils.get_entity_objects(TypeOfMeal)[0]

        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            response = await ac.delete(
                f"{self.route}/{type_of_meal_item['id']}",
                headers={"Authorization": f"Bearer {user_admin.access_token}"},
            )

        assert response.status_code == HTTP_200_OK

        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            response = await ac.get(
                f"/{CONTROLLER}/get/{type_of_meal_item['id']}",
                headers={"Authorization": f"Bearer {user_admin.access_token}"},
            )

        assert response.status_code == HTTP_404_NOT_FOUND

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Delete type of meal already deleted")
    async def test_delete_type_of_meal_already_deleted(
        self, user_admin: Optional[LoginPayloadDto]
    ) -> None:
        type_of_meal_item = self.db_test_utils.get_entity_objects(TypeOfMeal)[0]

        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            assert (
                await ac.delete(
                    f"{self.route}/{type_of_meal_item['id']}",
                    headers={"Authorization": f"Bearer {user_admin.access_token}"},
                )
            ).status_code == HTTP_404_NOT_FOUND

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Delete type of meal without authentication")
    async def test_no_authentication(self) -> None:
        type_of_meal_item = self.db_test_utils.get_entity_objects(TypeOfMeal)[1]
        await self.del_no_authentication(f"{self.route}/{type_of_meal_item['id']}")

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Delete type of meal without required authentication")
    async def test_different_required_authentication(
        self, user_common: Optional[LoginPayloadDto]
    ) -> None:
        type_of_meal_item = self.db_test_utils.get_entity_objects(TypeOfMeal)[1]
        await self.del_different_required_authentication(
            f"{self.route}/{type_of_meal_item['id']}", user_common
        )


@pytest.mark.describe(f"PATCH Route: /{CONTROLLER}/update/<id>")
class TestUpdateFood(TestBaseE2E):
    route = f"/{CONTROLLER}/update"

    @pytest.mark.asyncio
    @pytest.mark.it("Success: Update type of meal")
    async def test_update_type_of_meal(self, user_admin: Optional[LoginPayloadDto]) -> None:
        type_of_meal_item = self.db_test_utils.get_entity_objects(TypeOfMeal)[1]

        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            assert (
                await ac.patch(
                    f"{self.route}/{type_of_meal_item['id']}",
                    json={"description": "Big Meals updated"},
                    headers={"Authorization": f"Bearer {user_admin.access_token}"},
                )
            ).status_code == HTTP_200_OK

        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            response = await ac.get(
                f"/{CONTROLLER}/get/{type_of_meal_item['id']}",
                headers={"Authorization": f"Bearer {user_admin.access_token}"},
            )

        data = response.json()

        assert response.status_code == HTTP_200_OK
        assert data["description"] == "Big Meals updated"

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Update type fo meal without authentication")
    async def test_no_authentication(self) -> None:
        type_of_meal_item = self.db_test_utils.get_entity_objects(TypeOfMeal)[1]
        await self.patch_no_authentication(f"{self.route}/{type_of_meal_item['id']}")

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Update food without required authentication")
    async def test_different_required_authentication(
        self, user_common: Optional[LoginPayloadDto]
    ) -> None:
        type_of_meal_item = self.db_test_utils.get_entity_objects(TypeOfMeal)[1]
        await self.patch_different_required_authentication(
            f"{self.route}/{type_of_meal_item['id']}", user_common
        )
