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
from src.modules.domain.item.entities.item_entity import Item
from src.modules.domain.item.entities.item_has_food_entity import ItemHasFood
from src.modules.domain.item.services.item_service import ItemService
from src.modules.infrastructure.auth.dto.login_payload_dto import LoginPayloadDto
from test.test_base_e2e import TestBaseE2E

CONTROLLER = "item"
item_service = ItemService()


@pytest.mark.describe(f"POST Route: /{CONTROLLER}/create")
class TestCreateItem(TestBaseE2E):
    route = f"/{CONTROLLER}/create"

    @pytest.mark.asyncio
    @pytest.mark.it("Success: Create an item")
    async def test_create_item_one_food(self, user_admin: Optional[LoginPayloadDto]) -> None:
        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            response = await ac.post(
                self.route,
                json={
                    "description": "Item 1",
                    "foods": [
                        {"amount_grams": 200, "food": "950d760f-ba5c-44ca-b4ec-313510e59beb"}
                    ],
                },
                headers={"Authorization": f"Bearer {user_admin.access_token}"},
            )

        data = response.json()

        assert response.status_code == HTTP_201_CREATED
        assert [hasattr(data, attr_name) for attr_name in ["id", "foods"]]
        assert len(data["foods"]) == 1
        assert data["foods"][0] == "950d760f-ba5c-44ca-b4ec-313510e59beb"

        new_item = self.db_test_utils.db.query(Item).where(Item.id == data["id"]).first()
        assert len(new_item.foods) == 1
        assert new_item.foods[0].amount_grams == 200

    @pytest.mark.asyncio
    @pytest.mark.it("Success: Create an item with multiples foods")
    async def test_create_item_multiples_food(self, user_admin: Optional[LoginPayloadDto]) -> None:
        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            response = await ac.post(
                self.route,
                json={
                    "description": "Item Many Foods",
                    "foods": [
                        {"amount_grams": 200, "food": "950d760f-ba5c-44ca-b4ec-313510e59beb"},
                        {"amount_grams": 150, "food": "e3ff57d6-eb77-48de-bb49-ff9201d95926"},
                    ],
                },
                headers={"Authorization": f"Bearer {user_admin.access_token}"},
            )

        data = response.json()

        assert response.status_code == HTTP_201_CREATED
        assert [hasattr(data, attr_name) for attr_name in ["id", "foods"]]
        assert len(data["foods"]) == 2
        assert (
            "950d760f-ba5c-44ca-b4ec-313510e59beb" and "e3ff57d6-eb77-48de-bb49-ff9201d95926"
        ) in data["foods"]

        new_item = self.db_test_utils.db.query(Item).where(Item.id == data["id"]).first()
        assert len(new_item.foods) == 2

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Create a item with deleted food")
    async def test_create_item_with_deleted_food(
        self, user_admin: Optional[LoginPayloadDto]
    ) -> None:
        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            assert (
                await ac.post(
                    self.route,
                    json={
                        "description": "Item Deleted Food",
                        "foods": [
                            {"amount_grams": 200, "food": "0e8dbb8d-bf41-484d-90af-7c44fc4cb6fc"}
                        ],
                    },
                    headers={"Authorization": f"Bearer {user_admin.access_token}"},
                )
            ).status_code == HTTP_404_NOT_FOUND

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Create a item without required fields")
    async def test_create_item_without_required_field(
        self, user_admin: Optional[LoginPayloadDto]
    ) -> None:
        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            response = await ac.post(
                self.route,
                json={"description": "Item Deleted Food"},
                headers={"Authorization": f"Bearer {user_admin.access_token}"},
            )

        data = response.json()

        assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY
        assert data["detail"][0]["msg"] == "field required"
        assert data["detail"][0]["loc"] == ["body", "foods"]

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Create a food without required authorization")
    async def test_create_item_without_required_authorization(
        self, user_common: Optional[LoginPayloadDto], user_nutritionist: Optional[LoginPayloadDto]
    ) -> None:
        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            assert (
                await ac.post(
                    self.route,
                    json={
                        "description": "Item User",
                        "foods": [
                            {"amount_grams": 200, "food": "950d760f-ba5c-44ca-b4ec-313510e59beb"}
                        ],
                    },
                    headers={"Authorization": f"Bearer {user_common.access_token}"},
                )
            ).status_code == HTTP_403_FORBIDDEN


@pytest.mark.describe(f"GET Route: /{CONTROLLER}/get")
class TestGetAllItems(TestBaseE2E):
    route = f"/{CONTROLLER}/get"

    @pytest.mark.asyncio
    @pytest.mark.it("Success: Get a list of all items")
    async def test_get_items(self, user_admin: Optional[LoginPayloadDto]) -> None:
        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            response = await ac.get(
                self.route,
                headers={"Authorization": f"Bearer {user_admin.access_token}"},
            )

        body = response.json()
        data = body["data"]

        assert response.status_code == HTTP_200_OK
        assert body["count"] >= 2

        for item in data:
            if item["id"] == "a903fd03-26a5-449f-99f4-e83ea35d70e6":
                assert item["description"] == "Item 1"

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Get a list of all item without authentication")
    async def test_no_authentication(self) -> None:
        await self.get_no_authentication(self.route)

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Get a list of all item with non required authentication")
    async def test_different_required_authentication(
        self, user_common: Optional[LoginPayloadDto]
    ) -> None:
        await self.get_different_required_authentication(self.route, user_common)


@pytest.mark.describe(f"GET Route: /{CONTROLLER}/get/<id>")
class TestGetItemById(TestBaseE2E):
    route = f"/{CONTROLLER}/get/"

    @pytest.mark.asyncio
    @pytest.mark.it("Success: Get one item by id")
    async def test_get_item_by_id(self, user_admin: Optional[LoginPayloadDto]) -> None:
        item = self.db_test_utils.get_entity_objects(Item)[0]

        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            response = await ac.get(
                self.route + f"{item['id']}",
                headers={"Authorization": f"Bearer {user_admin.access_token}"},
            )

        data: dict = response.json()

        assert response.status_code == HTTP_200_OK
        assert isinstance(data, dict)
        assert data["id"] == item["id"]
        assert data["description"] == item["description"]

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Get one item without authentication")
    async def test_no_authentication(self) -> None:
        await self.get_no_authentication(self.route)

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Get one item with non required authentication")
    async def test_different_required_authentication(
        self, user_common: Optional[LoginPayloadDto]
    ) -> None:
        await self.get_different_required_authentication(self.route, user_common)


@pytest.mark.describe(f"DELETE Route: /{CONTROLLER}/delete/<id>")
class TestDeleteItem(TestBaseE2E):
    route = f"/{CONTROLLER}/delete"

    @pytest.mark.asyncio
    @pytest.mark.it("Success: Delete Item")
    async def test_delete_item(self, user_admin: Optional[LoginPayloadDto]) -> None:
        item = self.db_test_utils.get_entity_objects(Item)[1]

        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            response = await ac.delete(
                f"{self.route}/{item['id']}",
                headers={"Authorization": f"Bearer {user_admin.access_token}"},
            )

        data: dict = response.json()

        assert response.status_code == HTTP_200_OK
        assert data["affected"] >= 3

        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            response = await ac.get(
                f"/{CONTROLLER}/get/{item['id']}",
                headers={"Authorization": f"Bearer {user_admin.access_token}"},
            )

        assert response.status_code == HTTP_404_NOT_FOUND

    @pytest.mark.asyncio
    @pytest.mark.it("Success: Check if all relation from deleted item, was also deleted")
    async def test_delete_item_relations(self, user_admin: Optional[LoginPayloadDto]) -> None:
        deleted_item = self.db_test_utils.get_entity_objects(Item)[1]
        all_item_has_food = self.db_test_utils.get_entity_objects(ItemHasFood)

        deleted_item_has_food = [
            item for item in all_item_has_food if item["item_id"] == deleted_item["id"]
        ]

        for item in deleted_item_has_food:
            assert (
                self.db_test_utils.db.query(ItemHasFood).where(ItemHasFood.id == item["id"]).first()
                is None
            )

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Delete item already deleted")
    async def test_delete_item_already_deleted(self, user_admin: Optional[LoginPayloadDto]) -> None:
        item = self.db_test_utils.get_entity_objects(Item)[1]

        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            assert (
                await ac.delete(
                    f"{self.route}/{item['id']}",
                    headers={"Authorization": f"Bearer {user_admin.access_token}"},
                )
            ).status_code == HTTP_404_NOT_FOUND

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Delete item without authentication")
    async def test_no_authentication(self) -> None:
        item = self.db_test_utils.get_entity_objects(Item)[0]
        await self.del_no_authentication(f"{self.route}/{item['id']}")

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Delete item without required authentication")
    async def test_different_required_authentication(
        self, user_common: Optional[LoginPayloadDto]
    ) -> None:
        item = self.db_test_utils.get_entity_objects(Item)[0]
        await self.del_different_required_authentication(f"{self.route}/{item['id']}", user_common)


@pytest.mark.describe(f"PATCH Route: /{CONTROLLER}/update/<id>")
class TestUpdateItem(TestBaseE2E):
    route = f"/{CONTROLLER}/update"

    @pytest.mark.asyncio
    @pytest.mark.it("Success: Update an item")
    async def test_update_item(self, user_admin: Optional[LoginPayloadDto]) -> None:
        item = self.db_test_utils.get_entity_objects(Item)[0]

        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            response = await ac.patch(
                f"{self.route}/{item['id']}",
                json={
                    "description": "Item 2 Updated",
                    "foods": [
                        {"amount_grams": 150, "food": "e3ff57d6-eb77-48de-bb49-ff9201d95926"},
                        {"amount_grams": 90, "food": "950d760f-ba5c-44ca-b4ec-313510e59beb"},
                    ],
                },
                headers={"Authorization": f"Bearer {user_admin.access_token}"},
            )

        assert response.status_code == HTTP_200_OK
        data = response.json()
        assert data["affected"] == 3

        async with AsyncClient(app=app, base_url=self.base_url) as ac:
            response = await ac.get(
                f"/{CONTROLLER}/get/{item['id']}",
                headers={"Authorization": f"Bearer {user_admin.access_token}"},
            )

        data = response.json()

        assert response.status_code == HTTP_200_OK
        assert data["description"] == "Item 2 Updated"
        assert len(data["foods"]) == 2

        if data["foods"][0]["food"]["id"] == "e3ff57d6-eb77-48de-bb49-ff9201d95926":
            assert data["foods"][0]["amount_grams"] == 150
            assert data["foods"][1]["amount_grams"] == 90
            assert data["foods"][1]["food"]["id"] == "950d760f-ba5c-44ca-b4ec-313510e59beb"

        else:
            assert data["foods"][0]["food"]["id"] == "950d760f-ba5c-44ca-b4ec-313510e59beb"
            assert data["foods"][0]["amount_grams"] == 90

            assert data["foods"][1]["amount_grams"] == 150
            assert data["foods"][1]["food"]["id"] == "e3ff57d6-eb77-48de-bb49-ff9201d95926"

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Update an item without authentication")
    async def test_no_authentication(self) -> None:
        item = self.db_test_utils.get_entity_objects(Item)[0]
        await self.patch_no_authentication(f"{self.route}/{item['id']}")

    @pytest.mark.asyncio
    @pytest.mark.it("Failure: Update an item without required authentication")
    async def test_different_required_authentication(
        self, user_common: Optional[LoginPayloadDto]
    ) -> None:
        item = self.db_test_utils.get_entity_objects(Item)[0]
        await self.patch_different_required_authentication(
            f"{self.route}/{item['id']}", user_common
        )
