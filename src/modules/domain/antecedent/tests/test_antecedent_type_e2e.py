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
from src.modules.domain.antecedent.entities.antecedent_type_entity import AntecedentType
from src.modules.domain.antecedent.services.antecedent_service import AntecedentService
from src.modules.domain.antecedent.services.antecedent_type_service import AntecedentTypeService
from src.modules.infrastructure.auth.dto.login_payload_dto import LoginPayloadDto
from test.test_base_e2e import TestBaseE2E

CONTROLLER = "antecedent-type"
antecedent_type_service = AntecedentTypeService()


@pytest.mark.describe(f"POST Route: /{CONTROLLER}/create")
class TestCreateAntecedentType(TestBaseE2E):
    route = f"/{CONTROLLER}/create"

    @pytest.mark.asyncio
    @pytest.mark.it("Success: Create an antecedent type")
    async def test_create_new_antecedent_type(self, user_admin: Optional[LoginPayloadDto]) -> None:
        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            response = await ac.post(
                self.route,
                json={
                    "description": "Antecedent Type Test",
                },
                headers={"Authorization": f"Bearer {user_admin.access_token}"},
            )

        data = response.json()

        assert response.status_code == HTTP_201_CREATED
        assert [hasattr(data, attr_name) for attr_name in ["id", "description"]]
        assert data["description"] == "Antecedent Type Test"

        type_of_meal_dto = await antecedent_type_service.find_one_antecedent_type(
            data["id"], self.db_test_utils.db
        )

        assert type_of_meal_dto is not None
        assert type_of_meal_dto.description == data["description"]

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Create an antecedent type without required fields")
    async def test_create_antecedent_type_without_required_field(
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
    @pytest.mark.it("Failure: Create an antecedent type without required authorization")
    async def test_create_type_of_meal_without_required_authorization(
        self, user_common: Optional[LoginPayloadDto], user_nutritionist: Optional[LoginPayloadDto]
    ) -> None:
        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            assert (
                await ac.post(
                    self.route,
                    json={
                        "description": "Antecedent Type Test 2",
                    },
                    headers={"Authorization": f"Bearer {user_common.access_token}"},
                )
            ).status_code == HTTP_403_FORBIDDEN


@pytest.mark.describe(f"GET Route: /{CONTROLLER}/get")
class TestGetAllAntecedentType(TestBaseE2E):
    route = f"/{CONTROLLER}/get"

    @pytest.mark.asyncio
    @pytest.mark.it("Success: Get a list of all antecedent type")
    async def test_get_antecedent_types(self, user_admin: Optional[LoginPayloadDto]) -> None:
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
            if type_of_meal["id"] == "d1a6f6e7-fab1-4525-be7f-1c3a0ae6e997":
                assert type_of_meal["description"] == "Antecedent Type 2"

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Get a list of all antecedent types without authentication")
    async def test_no_authentication(self) -> None:
        await self.get_no_authentication(self.route)

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Get a list of all antecedent types with non required authentication")
    async def test_different_required_authentication(
        self, user_common: Optional[LoginPayloadDto]
    ) -> None:
        await self.get_different_required_authentication(self.route, user_common)


@pytest.mark.describe(f"GET Route: /{CONTROLLER}/get/<id>")
class TestGetAntecedentTypeById(TestBaseE2E):
    route = f"/{CONTROLLER}/get/"

    @pytest.mark.asyncio
    @pytest.mark.it("Success: Get one antecedent type by id")
    async def test_get_antecedent_type_by_id(self, user_admin: Optional[LoginPayloadDto]) -> None:
        antecedent_type_item = self.db_test_utils.get_entity_objects(AntecedentType)[0]

        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            response = await ac.get(
                self.route + f"{antecedent_type_item['id']}",
                headers={"Authorization": f"Bearer {user_admin.access_token}"},
            )

        data: dict = response.json()

        assert response.status_code == HTTP_200_OK
        assert isinstance(data, dict)
        assert data["id"] == antecedent_type_item["id"]
        assert data["description"] == antecedent_type_item["description"]

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Get one antecedent type without authentication")
    async def test_no_authentication(self) -> None:
        antecedent_type_item = self.db_test_utils.get_entity_objects(AntecedentType)[0]
        await self.get_no_authentication(self.route + f"{antecedent_type_item['id']}")

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Get one antecedent type with non required authentication")
    async def test_different_required_authentication(
        self, user_common: Optional[LoginPayloadDto]
    ) -> None:
        antecedent_type_item = self.db_test_utils.get_entity_objects(AntecedentType)[0]
        await self.get_different_required_authentication(
            self.route + f"{antecedent_type_item['id']}", user_common
        )


@pytest.mark.describe(f"DELETE Route: /{CONTROLLER}/delete/<id>")
class TestDeleteAntecedentType(TestBaseE2E):
    route = f"/{CONTROLLER}/delete"

    @pytest.mark.asyncio
    @pytest.mark.it("Success: Delete antecedent type")
    async def test_delete_antecedent_type(self, user_admin: Optional[LoginPayloadDto]) -> None:
        antecedent_type_item = self.db_test_utils.get_entity_objects(AntecedentType)[0]

        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            response = await ac.delete(
                f"{self.route}/{antecedent_type_item['id']}",
                headers={"Authorization": f"Bearer {user_admin.access_token}"},
            )

        assert response.status_code == HTTP_200_OK

        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            response = await ac.get(
                f"/{CONTROLLER}/get/{antecedent_type_item['id']}",
                headers={"Authorization": f"Bearer {user_admin.access_token}"},
            )

        assert response.status_code == HTTP_404_NOT_FOUND

    @pytest.mark.asyncio
    @pytest.mark.it("Success: Check if all relation from antecedent type, was deleted")
    async def test_delete_antecedent_type_relations(
        self, user_admin: Optional[LoginPayloadDto], user_common: Optional[LoginPayloadDto]
    ) -> None:
        antecedent_type_item = self.db_test_utils.get_entity_objects(AntecedentType)[0]
        antecedent_service = AntecedentService()
        response = await antecedent_service.antecedent_repository.find(
            {"where": Antecedent.antecedent_type_id == antecedent_type_item["id"]},
            self.db_test_utils.db,
        )
        assert isinstance(response, list)
        assert len(response) == 0

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Delete antecedent type already deleted")
    async def test_delete_antecedent_type_already_deleted(
        self, user_admin: Optional[LoginPayloadDto]
    ) -> None:
        antecedent_type_item = self.db_test_utils.get_entity_objects(AntecedentType)[0]

        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            assert (
                await ac.delete(
                    f"{self.route}/{antecedent_type_item['id']}",
                    headers={"Authorization": f"Bearer {user_admin.access_token}"},
                )
            ).status_code == HTTP_404_NOT_FOUND

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Delete antecedent type without authentication")
    async def test_no_authentication(self) -> None:
        antecedent_type_item = self.db_test_utils.get_entity_objects(AntecedentType)[1]
        await self.del_no_authentication(f"{self.route}/{antecedent_type_item['id']}")

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Delete antecedent type without required authentication")
    async def test_different_required_authentication(
        self, user_common: Optional[LoginPayloadDto]
    ) -> None:
        antecedent_type_item = self.db_test_utils.get_entity_objects(AntecedentType)[1]
        await self.del_different_required_authentication(
            f"{self.route}/{antecedent_type_item['id']}", user_common
        )


@pytest.mark.describe(f"PATCH Route: /{CONTROLLER}/update/<id>")
class TestUpdateAntecedentType(TestBaseE2E):
    route = f"/{CONTROLLER}/update"

    @pytest.mark.asyncio
    @pytest.mark.it("Success: Update antecedent type")
    async def test_update_antecedent_type(self, user_admin: Optional[LoginPayloadDto]) -> None:
        antecedent_type_item = self.db_test_utils.get_entity_objects(AntecedentType)[1]

        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            assert (
                await ac.patch(
                    f"{self.route}/{antecedent_type_item['id']}",
                    json={"description": "Antecedent Type 2 Updated"},
                    headers={"Authorization": f"Bearer {user_admin.access_token}"},
                )
            ).status_code == HTTP_200_OK

        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            response = await ac.get(
                f"/{CONTROLLER}/get/{antecedent_type_item['id']}",
                headers={"Authorization": f"Bearer {user_admin.access_token}"},
            )

        data = response.json()

        assert response.status_code == HTTP_200_OK
        assert data["description"] == "Antecedent Type 2 Updated"

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Update antecedent type without authentication")
    async def test_no_authentication(self) -> None:
        antecedent_type_item = self.db_test_utils.get_entity_objects(AntecedentType)[1]
        await self.patch_no_authentication(f"{self.route}/{antecedent_type_item['id']}")

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Update antecedent type without required authentication")
    async def test_different_required_authentication(
        self, user_common: Optional[LoginPayloadDto]
    ) -> None:
        antecedent_type_item = self.db_test_utils.get_entity_objects(AntecedentType)[1]
        await self.patch_different_required_authentication(
            f"{self.route}/{antecedent_type_item['id']}", user_common
        )
