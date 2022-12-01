from typing import Optional

import pytest
from _pytest.fixtures import FixtureRequest
from httpx import AsyncClient, QueryParams
from sqlalchemy.exc import IntegrityError
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_422_UNPROCESSABLE_ENTITY,
)

from src.main import app
from src.modules.domain.personal_data.services.personal_data_service import PersonalDataService
from src.modules.infrastructure.auth.dto.login_payload_dto import LoginPayloadDto
from test.test_base_e2e import TestBaseE2E

CONTROLLER = "personal-data"
personal_data_service = PersonalDataService()


@pytest.mark.describe(f"POST Route: /{CONTROLLER}/create")
class TestCreatePersonalData(TestBaseE2E):
    route = f"/{CONTROLLER}/create"

    @pytest.mark.asyncio
    @pytest.mark.it("Success: Create a personal data")
    async def test_create_new_personal_data(
        self, user_nutritionist: Optional[LoginPayloadDto]
    ) -> None:
        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            response = await ac.post(
                self.route,
                json={
                    "first_name": "Henrique",
                    "last_name": "Nutritionist",
                    "birthday": "1999-12-06",
                    "occupation": "Nutritionist",
                    "bedtime": "22:00:00",
                    "wake_up": "09:30:00",
                    "activity_level": "7783cab2-4115-4540-bf14-5a2a9e8c006c",
                    "user": "4fbc9c6a-8103-417b-9e76-2856d247b694",
                },
                headers={"Authorization": f"Bearer {user_nutritionist.access_token}"},
            )

        assert response.status_code == HTTP_201_CREATED

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Create two personal data to the same user")
    async def test_create_personal_data_same_user(
        self, user_nutritionist: Optional[LoginPayloadDto]
    ) -> None:
        with pytest.raises(IntegrityError) as e_info:
            async with AsyncClient(app=app, base_url=self.base_url) as ac:
                await ac.post(
                    self.route,
                    json={
                        "first_name": "Henrique",
                        "last_name": "Nutritionist 2",
                        "birthday": "1999-12-06",
                        "occupation": "Nutritionist",
                        "bedtime": "22:00:00",
                        "wake_up": "09:30:00",
                        "activity_level": "7783cab2-4115-4540-bf14-5a2a9e8c006c",
                        "user": "4fbc9c6a-8103-417b-9e76-2856d247b694",
                    },
                    headers={"Authorization": f"Bearer {user_nutritionist.access_token}"},
                )

        assert e_info.type == IntegrityError

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Create a personal data without required fields")
    async def test_create_personal_data_without_required_field(
        self, user_nutritionist: Optional[LoginPayloadDto]
    ) -> None:
        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            response = await ac.post(
                self.route,
                json={
                    "first_name": "Henrique",
                    "last_name": "Nutritionist",
                    "birthday": "1999-12-06",
                    "occupation": "Nutritionist",
                    "bedtime": "22:00:00",
                    "wake_up": "09:30:00",
                    "activity_level": "7783cab2-4115-4540-bf14-5a2a9e8c006c",
                },
                headers={"Authorization": f"Bearer {user_nutritionist.access_token}"},
            )

        data = response.json()

        assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY
        assert data["detail"][0]["msg"] == "field required"
        assert data["detail"][0]["loc"] == ["body", "user"]

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Create a personal data without required authorization")
    async def test_create_personal_data_without_required_authorization(
        self, user_common: Optional[LoginPayloadDto], user_admin: Optional[LoginPayloadDto]
    ) -> None:
        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            assert (
                await ac.post(
                    self.route,
                    json={
                        "first_name": "Henrique",
                        "last_name": "Nutritionist",
                        "birthday": "1999-12-06",
                        "occupation": "Nutritionist",
                        "bedtime": "22:00:00",
                        "wake_up": "09:30:00",
                        "activity_level": "7783cab2-4115-4540-bf14-5a2a9e8c006c",
                        "user": "09cdf815-9cda-4a87-8ae9-34c06f915278",
                    },
                    headers={"Authorization": f"Bearer {user_common.access_token}"},
                )
            ).status_code == HTTP_403_FORBIDDEN


@pytest.mark.describe(f"GET Route: /{CONTROLLER}/me/get")
class TestGetUserPersonalData(TestBaseE2E):
    route = f"/{CONTROLLER}/me/get"

    @pytest.mark.asyncio
    @pytest.mark.it("Success: Get current user personal data")
    async def test_get_current_user_personal_data(
        self, user_common: Optional[LoginPayloadDto]
    ) -> None:
        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            response = await ac.get(
                self.route,
                headers={"Authorization": f"Bearer {user_common.access_token}"},
            )

        data = response.json()

        assert response.status_code == HTTP_200_OK
        assert data["user"]["id"] == str(user_common.user.id)

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Get current user without authentication")
    async def test_no_authentication(self) -> None:
        await self.get_no_authentication(self.route)

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Get current user data without personal data")
    async def test_different_required_authentication(
        self, user_nutritionist: Optional[LoginPayloadDto]
    ) -> None:
        await self.get_different_required_authentication(self.route, user_nutritionist)


@pytest.mark.describe(f"GET Route: /{CONTROLLER}/users/get/")
class TestGetSeveralPersonalDataByUserId(TestBaseE2E):
    route = f"/{CONTROLLER}/users/get/"

    @pytest.mark.asyncio
    @pytest.mark.it("Success: Get one personal data by user id")
    async def test_get_one_personal_data_by_user_id(
        self, user_nutritionist: Optional[LoginPayloadDto], user_common: Optional[LoginPayloadDto]
    ) -> None:
        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            response = await ac.get(
                self.route,
                params=[("users_id", user_common.user.id)],
                headers={"Authorization": f"Bearer {user_nutritionist.access_token}"},
            )

        data = response.json()

        assert response.status_code == HTTP_200_OK
        assert isinstance(data, list)
        assert data[0]["user"]["id"] == str(user_common.user.id)

    @pytest.mark.asyncio
    @pytest.mark.it("Success: Get several personal data by user id")
    async def test_get_several_personal_data_by_user_id(
        self, user_nutritionist: Optional[LoginPayloadDto], user_common: Optional[LoginPayloadDto]
    ) -> None:
        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            response = await ac.get(
                self.route,
                params=[
                    ("users_id", user_common.user.id),
                    ("users_id", "5fbffb2b-531c-4f79-9f76-4f44e2a1dc21"),
                ],
                headers={"Authorization": f"Bearer {user_nutritionist.access_token}"},
            )

        data = response.json()

        assert response.status_code == HTTP_200_OK
        assert isinstance(data, list)
        assert len(data) == 2
        assert data[1]["user"]["id"] == "5fbffb2b-531c-4f79-9f76-4f44e2a1dc21"

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Get several personal data without authentication")
    async def test_no_authentication(self, user_admin: Optional[LoginPayloadDto]) -> None:
        await self.get_no_authentication(self.route)

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Get several personal data with non required authentication")
    @pytest.mark.parametrize("user", ["user_common"])
    async def test_different_required_authentication(
        self, user: str, user_common: Optional[LoginPayloadDto], request: FixtureRequest
    ) -> None:
        user: LoginPayloadDto = request.getfixturevalue(user)
        await self.get_different_required_authentication(self.route, user)


@pytest.mark.describe(f"PATCH Route: /{CONTROLLER}/update/<user_id>")
class TestUpdatePersonalData(TestBaseE2E):
    route = f"/{CONTROLLER}/update/"

    @pytest.mark.asyncio
    @pytest.mark.it("Success: Update personal data")
    async def test_update_personal_data(
        self, user_common: Optional[LoginPayloadDto], user_nutritionist: Optional[LoginPayloadDto]
    ) -> None:
        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            response = await ac.patch(
                self.route + f"{user_common.user.id}",
                json={"occupation": None},
                headers={"Authorization": f"Bearer {user_nutritionist.access_token}"},
            )

        assert response.status_code == HTTP_200_OK

        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            response = await ac.get(
                f"/{CONTROLLER}/users/get/",
                params=[("users_id", user_common.user.id)],
                headers={"Authorization": f"Bearer {user_nutritionist.access_token}"},
            )

        data = response.json()[0]

        assert response.status_code == HTTP_200_OK
        assert data["occupation"] is None

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Update personal data without authentication")
    async def test_no_authentication(self, user_common: Optional[LoginPayloadDto]) -> None:
        await self.patch_no_authentication((self.route + f"{user_common.user.id}"))

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Update personal data without required authentication")
    async def test_no_required_authentication(self, user_common: Optional[LoginPayloadDto]) -> None:
        await self.patch_different_required_authentication(
            (self.route + f"{user_common.user.id}"), user_common
        )

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Update user without personal data")
    async def test_update_user_without_personal_data(
        self, user_admin: Optional[LoginPayloadDto], user_nutritionist: Optional[LoginPayloadDto]
    ) -> None:
        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            assert (
                await ac.patch(
                    self.route + f"{user_admin.user.id}",
                    json={"occupation": None},
                    headers={"Authorization": f"Bearer {user_nutritionist.access_token}"},
                )
            ).status_code == HTTP_404_NOT_FOUND
