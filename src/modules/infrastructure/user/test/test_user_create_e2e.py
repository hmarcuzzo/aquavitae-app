from typing import Optional

import pytest
from httpx import AsyncClient

from src.core.constants.enum.user_role import UserRole
from src.main import app
from src.modules.infrastructure.auth.dto.login_payload_dto import LoginPayloadDto
from test.utils.test_base_e2e import TestBaseE2E

CONTROLLER = "user"


@pytest.mark.describe(f"GET Route: /{CONTROLLER}/get")
class TestGetAllUsers(TestBaseE2E):
    route = f"/{CONTROLLER}/get"

    @pytest.mark.asyncio
    @pytest.mark.it("Success: Get a list of all existing users")
    async def test_get_all_users(self, user_admin: Optional[LoginPayloadDto]) -> None:
        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            response = await ac.get(
                self.route,
                headers={"Authorization": f"Bearer {user_admin.access_token}"},
            )

        data = response.json()

        assert response.status_code == 200
        assert len(data) >= 0

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Get a list of all users without authentication")
    async def test_no_authentication(self) -> None:
        await self.no_authentication(self.route)

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Get a list of all users with non required authentication")
    async def test_user_authentication(
        self, user_common: Optional[LoginPayloadDto], user_nutricionist: Optional[LoginPayloadDto]
    ) -> None:
        await self.different_required_authentication(self.route, [user_common, user_nutricionist])


@pytest.mark.describe(f"GET Route: /{CONTROLLER}/get/<id>")
class TestGetUserById(TestBaseE2E):
    route = f"/{CONTROLLER}/get/"

    @pytest.mark.asyncio
    @pytest.mark.it("Success: Get one user by id")
    async def test_get_user_by_id(self, user_admin: Optional[LoginPayloadDto]) -> None:
        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            response = await ac.get(
                self.route + "4fbc9c6a-8103-417b-9e76-2856d247b694",
                headers={"Authorization": f"Bearer {user_admin.access_token}"},
            )

        data: dict = response.json()

        assert response.status_code == 200
        assert isinstance(data, dict)
        assert data["id"] == "4fbc9c6a-8103-417b-9e76-2856d247b694"
        assert data["role"] == UserRole.NUTRICIONIST.value
        assert data["email"] == "henrique_nutri@gmail.com"

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Get one user without authentication")
    async def test_no_authentication(self) -> None:
        await self.no_authentication(self.route)

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Get one user with non required authentication")
    async def test_user_authentication(
        self, user_common: Optional[LoginPayloadDto], user_nutricionist: Optional[LoginPayloadDto]
    ) -> None:
        await self.different_required_authentication(self.route, [user_common, user_nutricionist])
