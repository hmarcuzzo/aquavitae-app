from typing import Optional

import pytest
from _pytest.fixtures import FixtureRequest
from httpx import AsyncClient
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_422_UNPROCESSABLE_ENTITY,
)

from src.main import app
from src.modules.domain.appointment.services.appointment_goal_service import AppointmentGoalService
from src.modules.infrastructure.auth.dto.login_payload_dto import LoginPayloadDto
from test.test_base_e2e import TestBaseE2E

CONTROLLER = "appointment-goal"
appointment_goal_service = AppointmentGoalService()


@pytest.mark.describe(f"POST Route: /{CONTROLLER}/create")
class TestCreateAppointmentGoal(TestBaseE2E):
    route = f"/{CONTROLLER}/create"

    @pytest.mark.asyncio
    @pytest.mark.it("Success: Create a appointment goal")
    async def test_create_new_appointment_goal_with_date(
        self, user_admin: Optional[LoginPayloadDto]
    ) -> None:
        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            response = await ac.post(
                self.route,
                json={
                    "description": "Goal 2",
                },
                headers={"Authorization": f"Bearer {user_admin.access_token}"},
            )

        data = response.json()

        assert response.status_code == HTTP_201_CREATED
        assert data["description"] == "Goal 2"

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Create a appointment goal without required fields")
    async def test_create_appointment_goal_without_required_field(
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
    @pytest.mark.it("Failure: Create a appointment goal without required authorization")
    async def test_create_appointment_goal_without_required_authorization(
        self, user_common: Optional[LoginPayloadDto], user_nutritionist: Optional[LoginPayloadDto]
    ) -> None:
        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            assert (
                await ac.post(
                    self.route,
                    json={
                        "description": "Goal 3",
                    },
                    headers={"Authorization": f"Bearer {user_common.access_token}"},
                )
            ).status_code == HTTP_403_FORBIDDEN

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Create a appointment goal without authorization")
    async def test_create_appointment_goal_without_authorization(self) -> None:
        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            assert (
                await ac.post(
                    self.route,
                    json={
                        "description": "Goal 3",
                    },
                )
            ).status_code == HTTP_401_UNAUTHORIZED


@pytest.mark.describe(f"GET Route: /{CONTROLLER}/get")
class TestGetAllAppointmentGoal(TestBaseE2E):
    route = f"/{CONTROLLER}/get"

    @pytest.mark.asyncio
    @pytest.mark.it("Success: Get all appointment goal")
    async def test_get_all_appointment_goal(
        self, user_nutritionist: Optional[LoginPayloadDto]
    ) -> None:
        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            response = await ac.get(
                self.route,
                headers={"Authorization": f"Bearer {user_nutritionist.access_token}"},
            )

        data = response.json()

        assert response.status_code == HTTP_200_OK
        assert isinstance(data, dict)
        assert data["data"][0]["id"] == "dcf18594-13a1-4f8d-be14-8a6149a941e7"

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Get appointment goal without authentication")
    async def test_no_authentication(
        self, user_common: Optional[LoginPayloadDto], user_admin: Optional[LoginPayloadDto]
    ) -> None:
        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            assert (await ac.get(self.route)).status_code == HTTP_401_UNAUTHORIZED

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Get appointment goal with non required authentication")
    @pytest.mark.parametrize("user", ["user_common"])
    async def test_different_required_authentication(
        self, user: str, user_common: Optional[LoginPayloadDto], request: FixtureRequest
    ) -> None:
        user: LoginPayloadDto = request.getfixturevalue(user)
        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            assert (
                await ac.get(
                    self.route,
                    headers={"Authorization": f"Bearer {user.access_token}"},
                )
            ).status_code == HTTP_403_FORBIDDEN


@pytest.mark.describe(f"GET Route: /{CONTROLLER}/get/<appointment_goal_id>")
class TestGetAppointmentGoalById(TestBaseE2E):
    route = f"/{CONTROLLER}/get/"

    @pytest.mark.asyncio
    @pytest.mark.it("Success: Get appointment goal by id")
    async def test_get_appointment_goal_by_id(
        self, user_nutritionist: Optional[LoginPayloadDto]
    ) -> None:
        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            response = await ac.get(
                self.route + "dcf18594-13a1-4f8d-be14-8a6149a941e7",
                headers={"Authorization": f"Bearer {user_nutritionist.access_token}"},
            )

        data = response.json()

        assert response.status_code == HTTP_200_OK
        assert data["id"] == "dcf18594-13a1-4f8d-be14-8a6149a941e7"

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Get appointment goal without authentication")
    async def test_no_authentication(
        self, user_common: Optional[LoginPayloadDto], user_admin: Optional[LoginPayloadDto]
    ) -> None:
        await self.get_no_authentication((self.route + "dcf18594-13a1-4f8d-be14-8a6149a941e7"))

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Get appointment goal with non required authentication")
    @pytest.mark.parametrize("user", ["user_common"])
    async def test_different_required_authentication(
        self, user: str, user_common: Optional[LoginPayloadDto], request: FixtureRequest
    ) -> None:
        user: LoginPayloadDto = request.getfixturevalue(user)
        await self.get_different_required_authentication(
            (self.route + "dcf18594-13a1-4f8d-be14-8a6149a941e7"), user
        )


@pytest.mark.describe(f"PATCH Route: /{CONTROLLER}/update/<appointment_goal_id>")
class TestUpdateAppointmentGoal(TestBaseE2E):
    route = f"/{CONTROLLER}/update/"

    @pytest.mark.asyncio
    @pytest.mark.it("Success: Update appointment goal")
    async def test_update_appointment_goal(self, user_admin: Optional[LoginPayloadDto]) -> None:
        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            response = await ac.patch(
                self.route + "dcf18594-13a1-4f8d-be14-8a6149a941e7",
                json={"description": "Goal 0"},
                headers={"Authorization": f"Bearer {user_admin.access_token}"},
            )

        assert response.status_code == HTTP_200_OK

        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            response = await ac.get(
                f"/{CONTROLLER}/get/dcf18594-13a1-4f8d-be14-8a6149a941e7",
                headers={"Authorization": f"Bearer {user_admin.access_token}"},
            )

        data = response.json()

        assert response.status_code == HTTP_200_OK
        assert data["description"] == "Goal 0"

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Update appointment goal without authentication")
    async def test_no_authentication(self, user_common: Optional[LoginPayloadDto]) -> None:
        await self.patch_no_authentication(self.route + "dcf18594-13a1-4f8d-be14-8a6149a941e7")

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Update appointment goal without required authentication")
    async def test_no_required_authentication(self, user_common: Optional[LoginPayloadDto]) -> None:
        await self.patch_different_required_authentication(
            (self.route + "dcf18594-13a1-4f8d-be14-8a6149a941e7"), user_common
        )


@pytest.mark.describe(f"DELETE Route: /{CONTROLLER}/delete/<appointment_goal_id>")
class TestDeleteAppointmentGoal(TestBaseE2E):
    route = f"/{CONTROLLER}/delete/"

    @pytest.mark.asyncio
    @pytest.mark.it("Success: Delete appointment goal")
    async def test_delete_appointment_goal(self, user_admin: Optional[LoginPayloadDto]) -> None:
        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            response = await ac.delete(
                self.route + "dcf18594-13a1-4f8d-be14-8a6149a941e7",
                headers={"Authorization": f"Bearer {user_admin.access_token}"},
            )

        assert response.status_code == HTTP_200_OK

        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            response = await ac.get(
                f"/{CONTROLLER}/get/" + "dcf18594-13a1-4f8d-be14-8a6149a941e7",
                headers={"Authorization": f"Bearer {user_admin.access_token}"},
            )

        assert response.status_code == HTTP_404_NOT_FOUND

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Delete the same appointment goal twice")
    async def test_delete_same_appointment_goal(
        self, user_admin: Optional[LoginPayloadDto]
    ) -> None:
        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            assert (
                await ac.delete(
                    self.route + "dcf18594-13a1-4f8d-be14-8a6149a941e7",
                    headers={"Authorization": f"Bearer {user_admin.access_token}"},
                )
            ).status_code == HTTP_404_NOT_FOUND

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Delete appointment goal without authentication")
    async def test_no_authentication(self) -> None:
        await self.del_no_authentication((self.route + "dcf18594-13a1-4f8d-be14-8a6149a941e7"))
