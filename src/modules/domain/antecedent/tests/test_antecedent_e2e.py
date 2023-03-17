from typing import Optional

import pytest
from httpx import AsyncClient
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_422_UNPROCESSABLE_ENTITY,
)

from src.main import app
from src.modules.domain.antecedent.entities.antecedent_entity import Antecedent
from src.modules.domain.antecedent.services.antecedent_service import AntecedentService
from src.modules.infrastructure.auth.dto.login_payload_dto import LoginPayloadDto
from test.test_base_e2e import TestBaseE2E

CONTROLLER = "antecedent"
antecedent_service = AntecedentService()


@pytest.mark.describe(f"POST Route: /{CONTROLLER}/create")
class TestCreateAntecedent(TestBaseE2E):
    route = f"/{CONTROLLER}/create"

    @pytest.mark.asyncio
    @pytest.mark.it("Success: Create an antecedent")
    async def test_create_new_antecedent(self, user_admin: Optional[LoginPayloadDto]) -> None:
        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            response = await ac.post(
                self.route,
                json={
                    "description": "Antecedent Test",
                    "antecedent_type": "d1a6f6e7-fab1-4525-be7f-1c3a0ae6e997",
                    "user": "5fbffb2b-531c-4f79-9f76-4f44e2a1dc21",
                },
                headers={"Authorization": f"Bearer {user_admin.access_token}"},
            )

        data = response.json()

        assert response.status_code == HTTP_201_CREATED
        assert [hasattr(data, attr_name) for attr_name in ["id", "description"]]
        assert data["description"] == "Antecedent Test"

        type_of_meal_dto = await antecedent_service.find_one_antecedent(
            data["id"], self.db_test_utils.db
        )

        assert type_of_meal_dto is not None
        assert type_of_meal_dto.description == data["description"]

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Create an antecedent without required fields")
    async def test_create_antecedent_without_required_field(
        self, user_admin: Optional[LoginPayloadDto]
    ) -> None:
        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            response = await ac.post(
                self.route,
                json={},
                headers={"Authorization": f"Bearer {user_admin.access_token}"},
            )

        data = response.json()

        assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY
        assert data["detail"][0]["msg"] == "field required"
        assert data["detail"][0]["loc"] == ["body", "description"]

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Create an antecedent without required authorization")
    async def test_create_type_of_meal_without_required_authorization(
        self, user_common: Optional[LoginPayloadDto], user_nutritionist: Optional[LoginPayloadDto]
    ) -> None:
        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            assert (
                await ac.post(
                    self.route,
                    json={
                        "description": "Antecedent Test 2",
                        "antecedent_type": "68041164-e1e9-49d7-8c5f-6626066de67b",
                        "user": "5fbffb2b-531c-4f79-9f76-4f44e2a1dc21",
                    },
                    headers={"Authorization": f"Bearer {user_common.access_token}"},
                )
            ).status_code == HTTP_403_FORBIDDEN


@pytest.mark.describe(f"GET Route: /{CONTROLLER}/get")
class TestGetAllAntecedent(TestBaseE2E):
    route = f"/{CONTROLLER}/get"

    @pytest.mark.asyncio
    @pytest.mark.it("Success: Get a list of all antecedents")
    async def test_get_antecedents(self, user_admin: Optional[LoginPayloadDto]) -> None:
        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            response = await ac.get(
                self.route,
                params={"columns": "description"},
                headers={"Authorization": f"Bearer {user_admin.access_token}"},
            )

        body = response.json()
        data = body["data"]

        assert response.status_code == HTTP_200_OK
        assert body["count"] >= 0

        for type_of_meal in data:
            if type_of_meal["id"] == "a241fd4a-4943-4406-bfa8-347c4a5df2d3":
                assert type_of_meal["description"] == "Antecedent 1"

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Get a list of all antecedents without authentication")
    async def test_no_authentication(self) -> None:
        await self.get_no_authentication(self.route)

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Get a list of all antecedents with non required authentication")
    async def test_different_required_authentication(
        self, user_common: Optional[LoginPayloadDto]
    ) -> None:
        await self.get_different_required_authentication(self.route, user_common)


@pytest.mark.describe(f"GET Route: /{CONTROLLER}/get/<id>")
class TestGetAntecedentById(TestBaseE2E):
    route = f"/{CONTROLLER}/get/"

    @pytest.mark.asyncio
    @pytest.mark.it("Success: Get one antecedent by id")
    async def test_get_antecedent_by_id(self, user_admin: Optional[LoginPayloadDto]) -> None:
        antecedent_item = self.db_test_utils.get_entity_objects(Antecedent)[0]

        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            response = await ac.get(
                self.route + f"{antecedent_item['id']}",
                headers={"Authorization": f"Bearer {user_admin.access_token}"},
            )

        data = response.json()

        assert response.status_code == HTTP_200_OK
        assert isinstance(data, dict)
        assert data["id"] == antecedent_item["id"]
        assert data["description"] == antecedent_item["description"]

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Get one antecedent without authentication")
    async def test_no_authentication(self) -> None:
        antecedent_item = self.db_test_utils.get_entity_objects(Antecedent)[0]
        await self.get_no_authentication(self.route + f"{antecedent_item['id']}")

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Get one antecedent with non required authentication")
    async def test_different_required_authentication(
        self, user_common: Optional[LoginPayloadDto]
    ) -> None:
        antecedent_item = self.db_test_utils.get_entity_objects(Antecedent)[0]
        await self.get_different_required_authentication(
            self.route + f"{antecedent_item['id']}", user_common
        )


@pytest.mark.describe(f"DELETE Route: /{CONTROLLER}/delete/<id>")
class TestDeleteAntecedent(TestBaseE2E):
    route = f"/{CONTROLLER}/delete"

    @pytest.mark.asyncio
    @pytest.mark.it("Success: Delete antecedent")
    async def test_delete_antecedent(self, user_admin: Optional[LoginPayloadDto]) -> None:
        antecedent_item = self.db_test_utils.get_entity_objects(Antecedent)[0]

        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            response = await ac.delete(
                f"{self.route}/{antecedent_item['id']}",
                headers={"Authorization": f"Bearer {user_admin.access_token}"},
            )

        assert response.status_code == HTTP_200_OK

        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            response = await ac.get(
                f"/{CONTROLLER}/get/{antecedent_item['id']}",
                headers={"Authorization": f"Bearer {user_admin.access_token}"},
            )

        assert response.status_code == HTTP_404_NOT_FOUND

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Delete antecedent already deleted")
    async def test_delete_antecedent_already_deleted(
        self, user_admin: Optional[LoginPayloadDto]
    ) -> None:
        antecedent_item = self.db_test_utils.get_entity_objects(Antecedent)[0]

        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            assert (
                await ac.delete(
                    f"{self.route}/{antecedent_item['id']}",
                    headers={"Authorization": f"Bearer {user_admin.access_token}"},
                )
            ).status_code == HTTP_404_NOT_FOUND

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Delete antecedent without authentication")
    async def test_no_authentication(self) -> None:
        antecedent_item = self.db_test_utils.get_entity_objects(Antecedent)[1]
        await self.del_no_authentication(f"{self.route}/{antecedent_item['id']}")

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Delete antecedent without required authentication")
    async def test_different_required_authentication(
        self, user_common: Optional[LoginPayloadDto]
    ) -> None:
        antecedent_item = self.db_test_utils.get_entity_objects(Antecedent)[1]
        await self.del_different_required_authentication(
            f"{self.route}/{antecedent_item['id']}", user_common
        )


@pytest.mark.describe(f"PATCH Route: /{CONTROLLER}/update/<id>")
class TestUpdateAntecedent(TestBaseE2E):
    route = f"/{CONTROLLER}/update"

    @pytest.mark.asyncio
    @pytest.mark.it("Success: Update antecedent")
    async def test_update_antecedent(self, user_admin: Optional[LoginPayloadDto]) -> None:
        antecedent_item = self.db_test_utils.get_entity_objects(Antecedent)[1]

        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            assert (
                await ac.patch(
                    f"{self.route}/{antecedent_item['id']}",
                    json={"description": "Antecedent 2 Updated"},
                    headers={"Authorization": f"Bearer {user_admin.access_token}"},
                )
            ).status_code == HTTP_200_OK

        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            response = await ac.get(
                f"/{CONTROLLER}/get/{antecedent_item['id']}",
                headers={"Authorization": f"Bearer {user_admin.access_token}"},
            )

        data = response.json()

        assert response.status_code == HTTP_200_OK
        assert data["description"] == "Antecedent 2 Updated"

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Update antecedent without authentication")
    async def test_no_authentication(self) -> None:
        antecedent_item = self.db_test_utils.get_entity_objects(Antecedent)[1]
        await self.patch_no_authentication(f"{self.route}/{antecedent_item['id']}")

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Update antecedent without required authentication")
    async def test_different_required_authentication(
        self, user_common: Optional[LoginPayloadDto]
    ) -> None:
        antecedent_item = self.db_test_utils.get_entity_objects(Antecedent)[1]
        await self.patch_different_required_authentication(
            f"{self.route}/{antecedent_item['id']}", user_common
        )
