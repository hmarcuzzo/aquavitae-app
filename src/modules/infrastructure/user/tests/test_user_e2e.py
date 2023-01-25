from typing import Optional

import pytest
from _pytest.fixtures import FixtureRequest
from httpx import AsyncClient
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_422_UNPROCESSABLE_ENTITY,
)

from src.core.constants.enum.user_role import UserRole
from src.main import app
from src.modules.domain.anthropometric_data.entities.anthropometric_data_entity import (
    AnthropometricData,
)
from src.modules.domain.anthropometric_data.services.anthropometric_data_service import (
    AnthropometricDataService,
)
from src.modules.domain.personal_data.services.personal_data_service import PersonalDataService
from src.modules.infrastructure.auth.dto.login_payload_dto import LoginPayloadDto
from src.modules.infrastructure.user.user_service import UserService
from test.test_base_e2e import TestBaseE2E

CONTROLLER = "user"
user_service = UserService()


@pytest.mark.describe(f"POST Route: /{CONTROLLER}/create")
class TestCreateUser(TestBaseE2E):
    route = f"/{CONTROLLER}/create"

    @pytest.mark.asyncio
    @pytest.mark.it("Success: Create a new user")
    async def test_create_new_user(self, user_admin: Optional[LoginPayloadDto]) -> None:
        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            response = await ac.post(
                self.route,
                json={
                    "email": "henrique_teste@gmail.com",
                    "password": "12345678",
                },
                headers={"Authorization": f"Bearer {user_admin.access_token}"},
            )

        data = response.json()

        assert response.status_code == HTTP_201_CREATED
        assert [hasattr(data, attr_name) for attr_name in ["id", "email", "role"]]
        assert data["email"] == "henrique_teste@gmail.com"
        assert data["role"] == UserRole.USER.value

        user_dto = await user_service.find_one_user(data["id"], self.db_test_utils.db)

        assert user_dto is not None
        assert user_dto.email == data["email"]

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Create a new user with email that already exists")
    async def test_create_user_with_same_email(self, user_admin: Optional[LoginPayloadDto]) -> None:
        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            assert (
                await ac.post(
                    self.route,
                    json={
                        "email": "henrique_teste@gmail.com",
                        "password": "12345678",
                    },
                    headers={"Authorization": f"Bearer {user_admin.access_token}"},
                )
            ).status_code == HTTP_400_BAD_REQUEST

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Create a user without required fields")
    async def test_create_user_without_required_field(
        self,
        user_common: Optional[LoginPayloadDto],
        user_nutritionist: Optional[LoginPayloadDto],
        user_admin: Optional[LoginPayloadDto],
    ) -> None:
        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            response = await ac.post(
                self.route,
                json={
                    "password": "12345678",
                },
                headers={"Authorization": f"Bearer {user_admin.access_token}"},
            )

        data = response.json()

        assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY
        assert data["detail"][0]["msg"] == "field required"
        assert data["detail"][0]["loc"] == ["body", "email"]


@pytest.mark.describe(f"POST Route: /{CONTROLLER}/with-role/create")
class TestCreateUserWithRole(TestBaseE2E):
    route = f"/{CONTROLLER}/with-role/create"

    @pytest.mark.asyncio
    @pytest.mark.it("Success: Create a new user with role in body")
    async def test_create_new_user_with_role(self, user_admin: Optional[LoginPayloadDto]) -> None:
        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            response = await ac.post(
                self.route,
                json={
                    "email": "henrique_teste_role@gmail.com",
                    "password": "12345678",
                    "role": UserRole.NUTRITIONIST.value,
                },
                headers={"Authorization": f"Bearer {user_admin.access_token}"},
            )

        data = response.json()

        assert response.status_code == HTTP_201_CREATED
        assert [hasattr(data, attr_name) for attr_name in ["id", "email", "role"]]
        assert data["email"] == "henrique_teste_role@gmail.com"
        assert data["role"] == UserRole.NUTRITIONIST.value

        user_dto = await user_service.find_one_user(data["id"], self.db_test_utils.db)

        assert user_dto is not None
        assert user_dto.email == data["email"]

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Create a user without required fields")
    async def test_create_user_without_required_field(
        self,
        user_common: Optional[LoginPayloadDto],
        user_nutritionist: Optional[LoginPayloadDto],
        user_admin: Optional[LoginPayloadDto],
    ) -> None:
        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            response = await ac.post(
                self.route,
                json={
                    "email": "henrique_teste_role@gmail.com",
                    "password": "12345678",
                },
                headers={"Authorization": f"Bearer {user_admin.access_token}"},
            )

        data = response.json()

        assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY
        assert data["detail"][0]["msg"] == "field required"
        assert data["detail"][0]["loc"] == ["body", "role"]


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

        assert response.status_code == HTTP_200_OK
        assert len(data["data"]) >= 0

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Get a list of all users without authentication")
    async def test_no_authentication(self) -> None:
        await self.get_no_authentication(self.route)

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Get a list of all users with non required authentication")
    @pytest.mark.parametrize("user", ["user_common", "user_nutritionist"])
    async def test_different_required_authentication(
        self, user: str, request: FixtureRequest
    ) -> None:
        user: LoginPayloadDto = request.getfixturevalue(user)
        await self.get_different_required_authentication(self.route, user)


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

        assert response.status_code == HTTP_200_OK
        assert isinstance(data, dict)
        assert data["id"] == "4fbc9c6a-8103-417b-9e76-2856d247b694"
        assert data["role"] == UserRole.NUTRITIONIST.value
        assert data["email"] == "henrique_nutri@gmail.com"

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Get one user without authentication")
    async def test_no_authentication(self) -> None:
        await self.get_no_authentication(self.route)

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Get one user with non required authentication")
    @pytest.mark.parametrize("user", ["user_common", "user_nutritionist"])
    async def test_different_required_authentication(
        self, user: str, request: FixtureRequest
    ) -> None:
        user: LoginPayloadDto = request.getfixturevalue(user)
        await self.get_different_required_authentication(self.route, user)


@pytest.mark.describe(f"DELETE Route: /{CONTROLLER}/delete")
class TestDeleteUser(TestBaseE2E):
    route = f"/{CONTROLLER}/delete"

    @pytest.mark.asyncio
    @pytest.mark.it("Success: Delete user common")
    async def test_delete_user_common(
        self, user_admin: Optional[LoginPayloadDto], user_common: Optional[LoginPayloadDto]
    ) -> None:
        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            response = await ac.delete(
                self.route,
                headers={"Authorization": f"Bearer {user_common.access_token}"},
            )

        assert response.status_code == HTTP_200_OK

        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            response = await ac.get(
                f"/{CONTROLLER}/get/" + str(user_common.user.id),
                headers={"Authorization": f"Bearer {user_admin.access_token}"},
            )

        assert response.status_code == HTTP_404_NOT_FOUND

    @pytest.mark.asyncio
    @pytest.mark.it("Success: Check if all relation from user common, was deleted")
    async def test_delete_user_common_relations(
        self, user_admin: Optional[LoginPayloadDto], user_common: Optional[LoginPayloadDto]
    ) -> None:
        personal_data_service = PersonalDataService()
        assert (
            await personal_data_service.find_one_personal_data(
                str(user_common.user.id), self.db_test_utils.db
            )
            is None
        )

        anthropometric_data_service = AnthropometricDataService()
        response = await anthropometric_data_service.get_all_user_anthropometric_data(
            {"where": AnthropometricData.user_id == user_common.user.id, "skip": 0, "take": 10},
            self.db_test_utils.db,
        )

        assert response.count == 0

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Delete the same user twice")
    async def test_delete_same_user(
        self, user_admin: Optional[LoginPayloadDto], user_common: Optional[LoginPayloadDto]
    ) -> None:
        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            assert (
                await ac.delete(
                    self.route,
                    headers={"Authorization": f"Bearer {user_common.access_token}"},
                )
            ).status_code == HTTP_404_NOT_FOUND

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Delete user without authentication")
    async def test_no_authentication(self) -> None:
        await self.del_no_authentication(self.route)


@pytest.mark.describe(f"PATCH Route: /{CONTROLLER}/update/<id>")
class TestUpdateUser(TestBaseE2E):
    route = f"/{CONTROLLER}/update"

    @pytest.mark.asyncio
    @pytest.mark.it("Success: Update user nutritionist")
    async def test_update_user_nutri(
        self, user_admin: Optional[LoginPayloadDto], user_nutritionist: Optional[LoginPayloadDto]
    ) -> None:
        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            response = await ac.patch(
                self.route,
                json={"email": "henrique_nutri_updated@gmail.com"},
                headers={"Authorization": f"Bearer {user_nutritionist.access_token}"},
            )

        assert response.status_code == HTTP_200_OK
        assert response.json()["affected"] >= 1

        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            response = await ac.get(
                f"/{CONTROLLER}/get/" + str(user_nutritionist.user.id),
                headers={"Authorization": f"Bearer {user_admin.access_token}"},
            )

        data = response.json()

        assert response.status_code == HTTP_200_OK
        assert data["email"] == "henrique_nutri_updated@gmail.com"

    @pytest.mark.asyncio
    @pytest.mark.it("Success: Update user with deleted user email")
    async def test_update_with_email_already_deleted(
        self, user_admin: Optional[LoginPayloadDto], user_nutritionist: Optional[LoginPayloadDto]
    ) -> None:
        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            response = await ac.patch(
                self.route,
                json={"email": "henrique_user@gmail.com"},
                headers={"Authorization": f"Bearer {user_nutritionist.access_token}"},
            )

        assert response.status_code == HTTP_200_OK

        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            response = await ac.get(
                f"/{CONTROLLER}/get/" + str(user_nutritionist.user.id),
                headers={"Authorization": f"Bearer {user_admin.access_token}"},
            )

        data = response.json()

        assert response.status_code == HTTP_200_OK
        assert data["email"] == "henrique_user@gmail.com"

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Update user with email that already exists")
    async def test_update_email_exists(
        self, user_admin: Optional[LoginPayloadDto], user_nutritionist: Optional[LoginPayloadDto]
    ) -> None:
        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            response = await ac.patch(
                self.route,
                json={"email": "henrique_admin@gmail.com"},
                headers={"Authorization": f"Bearer {user_nutritionist.access_token}"},
            )

        assert response.status_code == HTTP_400_BAD_REQUEST

        detail = response.json()["detail"][0]
        assert detail["msg"] == "Email already in use."

        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            response = await ac.get(
                f"/{CONTROLLER}/get/" + str(user_nutritionist.user.id),
                headers={"Authorization": f"Bearer {user_admin.access_token}"},
            )

        data = response.json()

        assert response.status_code == HTTP_200_OK
        assert data["email"] == "henrique_user@gmail.com"

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Update deleted user")
    async def test_delete_same_user(
        self, user_admin: Optional[LoginPayloadDto], user_common: Optional[LoginPayloadDto]
    ) -> None:
        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            assert (
                await ac.patch(
                    self.route,
                    json={"email": "henrique_user_updated@gmail.com"},
                    headers={"Authorization": f"Bearer {user_common.access_token}"},
                )
            ).status_code == HTTP_404_NOT_FOUND

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Update user without authentication")
    async def test_no_authentication(self) -> None:
        await self.patch_no_authentication(self.route)
