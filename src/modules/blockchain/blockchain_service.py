from datetime import datetime

from httpx import AsyncClient
from starlette.requests import Request

from src.modules.blockchain.utils import BlockchainUtils
from src.modules.infrastructure.auth.jwt_service import verify_token


class BlockchainService:
    def __init__(self):
        self.base_url = "http://localhost:5000"

    # -------------- PUBLIC METHODS --------------
    async def send_new_block(self, request: Request):
        body = self.__get_body_data(request)
        encrypted_body = BlockchainUtils.encrypt_data(body)
        signed_body = BlockchainUtils.sign(encrypted_body)

        try:
            async with AsyncClient(base_url=self.base_url) as ac:
                response = await ac.post(
                    "/add",
                    json={
                        "signature": signed_body,
                        "transaction_hash": encrypted_body.decode("utf-8"),
                    },
                )
            # data = response.json()
        except Exception:
            pass

    # -------------- PRIVATE METHODS --------------
    @staticmethod
    def __get_body_data(request: Request) -> dict:
        return {
            "timestamp": datetime.now().timestamp(),
            "method": request.method,
            "path": request.url.path,
            "user_id": verify_token(request.headers["Authorization"].split(" ")[1], "user_id")
            if "Authorization" in request.headers
            else None,
        }
