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
from src.modules.domain.personal_data.entities.activity_level_entity import ActivityLevel
from src.modules.domain.personal_data.services.activity_level_service import ActivityLevelService
from src.modules.infrastructure.auth.dto.login_payload_dto import LoginPayloadDto
from test.test_base_e2e import TestBaseE2E

CONTROLLER = "activity-level"
activity_level_service = ActivityLevelService()


@pytest.mark.describe(f"POST Route: /{CONTROLLER}/create")
class TestCreateActivityLevel(TestBaseE2E):
    route = f"/{CONTROLLER}/create"

    @pytest.mark.asyncio
    @pytest.mark.it("Success: Create a activity level")
    async def test_create_new_activity_level(self, user_admin: Optional[LoginPayloadDto]) -> None:
        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            response = await ac.post(
                self.route,
                json={"description": "Level 1", "factor": 1},
                headers={"Authorization": f"Bearer {user_admin.access_token}"},
            )

        data = response.json()

        assert response.status_code == HTTP_201_CREATED
        assert [hasattr(data, attr_name) for attr_name in ["id", "description", "factor"]]
        assert data["description"] == "Level 1"
        assert data["factor"] == 1

        activity_level_dto = await activity_level_service.find_one_activity_level(
            data["id"], self.db_test_utils.db
        )

        assert activity_level_dto is not None
        assert activity_level_dto.description == data["description"]

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Create a activity level without required fields")
    async def test_create_activity_level_without_required_field(
        self, user_admin: Optional[LoginPayloadDto]
    ) -> None:
        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            response = await ac.post(
                self.route,
                json={"description": "Level 1"},
                headers={"Authorization": f"Bearer {user_admin.access_token}"},
            )

        data = response.json()

        assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY
        assert data["detail"][0]["msg"] == "field required"
        assert data["detail"][0]["loc"] == ["body", "factor"]

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Create a activity level without required authorization")
    async def test_create_user_without_required_field(
        self, user_common: Optional[LoginPayloadDto], user_nutritionist: Optional[LoginPayloadDto]
    ) -> None:
        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            assert (
                await ac.post(
                    self.route,
                    json={"description": "Level 1", "factor": 1},
                    headers={"Authorization": f"Bearer {user_common.access_token}"},
                )
            ).status_code == HTTP_403_FORBIDDEN


@pytest.mark.describe(f"GET Route: /{CONTROLLER}/get")
class TestGetAllActivityLevel(TestBaseE2E):
    route = f"/{CONTROLLER}/get"

    @pytest.mark.asyncio
    @pytest.mark.it("Success: Get a list of all activity levels")
    async def test_get_all_users(self, user_admin: Optional[LoginPayloadDto]) -> None:
        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            response = await ac.get(
                self.route,
                headers={"Authorization": f"Bearer {user_admin.access_token}"},
            )

        data = response.json()

        assert response.status_code == HTTP_200_OK
        assert len(data) >= 0

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Get a list of all activity levels without authentication")
    async def test_no_authentication(self) -> None:
        await self.get_no_authentication(self.route)

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Get a list of all activity levels with non required authentication")
    @pytest.mark.parametrize("user", ["user_common", "user_nutritionist"])
    async def test_different_required_authentication(
        self, user: str, request: FixtureRequest
    ) -> None:
        user: LoginPayloadDto = request.getfixturevalue(user)
        await self.different_required_authentication(self.route, user)


@pytest.mark.describe(f"GET Route: /{CONTROLLER}/get/<id>")
class TestGetActivityLevelById(TestBaseE2E):
    route = f"/{CONTROLLER}/get/"

    @pytest.mark.asyncio
    @pytest.mark.it("Success: Get one user by id")
    async def test_get_activity_level_by_id(self, user_admin: Optional[LoginPayloadDto]) -> None:
        activity_item = self.db_test_utils.get_entity_objects(ActivityLevel)[1]

        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            response = await ac.get(
                self.route + f"{activity_item['id']}",
                headers={"Authorization": f"Bearer {user_admin.access_token}"},
            )

        data: dict = response.json()

        assert response.status_code == HTTP_200_OK
        assert isinstance(data, dict)
        assert data["id"] == activity_item["id"]
        assert data["factor"] == activity_item["factor"]
        assert data["description"] == activity_item["description"]

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Get one activity level without authentication")
    async def test_no_authentication(self) -> None:
        await self.get_no_authentication(self.route)

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Get one activity level with non required authentication")
    @pytest.mark.parametrize("user", ["user_common", "user_nutritionist"])
    async def test_different_required_authentication(
        self, user: str, request: FixtureRequest
    ) -> None:
        user: LoginPayloadDto = request.getfixturevalue(user)
        await self.different_required_authentication(self.route, user)


@pytest.mark.describe(f"DELETE Route: /{CONTROLLER}/delete")
class TestDeleteActivityLevel(TestBaseE2E):
    route = f"/{CONTROLLER}/delete"

    @pytest.mark.asyncio
    @pytest.mark.it("Success: Delete activity level")
    async def test_delete_activity_level(self, user_admin: Optional[LoginPayloadDto]) -> None:
        activity_item = self.db_test_utils.get_entity_objects(ActivityLevel)[1]

        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            response = await ac.delete(
                f"{self.route}/{activity_item['id']}",
                headers={"Authorization": f"Bearer {user_admin.access_token}"},
            )

        assert response.status_code == HTTP_200_OK

        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            response = await ac.get(
                f"/{CONTROLLER}/get/{activity_item['id']}",
                headers={"Authorization": f"Bearer {user_admin.access_token}"},
            )

        assert response.status_code == HTTP_404_NOT_FOUND

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Delete activity level without authentication")
    async def test_no_authentication(self) -> None:
        activity_item = self.db_test_utils.get_entity_objects(ActivityLevel)[1]
        await self.del_no_authentication(f"{self.route}/{activity_item['id']}")


@pytest.mark.describe(f"PATCH Route: /{CONTROLLER}/update/<id>")
class TestUpdateActivityLevel(TestBaseE2E):
    route = f"/{CONTROLLER}/update"

    @pytest.mark.asyncio
    @pytest.mark.it("Success: Update activity level")
    async def test_update_activity_level(self, user_admin: Optional[LoginPayloadDto]) -> None:
        activity_item = self.db_test_utils.get_entity_objects(ActivityLevel)[0]

        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            response = await ac.patch(
                f"{self.route}/{activity_item['id']}",
                json={"description": "Level 11"},
                headers={"Authorization": f"Bearer {user_admin.access_token}"},
            )

        assert response.status_code == HTTP_200_OK

        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            response = await ac.get(
                f"/{CONTROLLER}/get/{activity_item['id']}",
                headers={"Authorization": f"Bearer {user_admin.access_token}"},
            )

        data = response.json()

        assert response.status_code == HTTP_200_OK
        assert data["description"] == "Level 11"

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Update activity level without authentication")
    async def test_no_authentication(self) -> None:
        activity_item = self.db_test_utils.get_entity_objects(ActivityLevel)[0]
        await self.patch_no_authentication(f"{self.route}/{activity_item['id']}")
