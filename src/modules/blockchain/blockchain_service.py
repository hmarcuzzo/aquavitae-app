import json
import os
from datetime import datetime

from httpx import AsyncClient
from starlette.requests import Request

from config import ROOT_DIR
from src.modules.blockchain.utils import BlockchainUtils
from src.modules.infrastructure.auth.jwt_service import verify_token


class BlockchainService:
    def __init__(self):
        self.base_url = "http://localhost:5000"
        self.transactions_log_file = ROOT_DIR + os.path.join("/src/static/doc/system_logs.txt")

    # -------------- PUBLIC METHODS --------------
    async def send_new_block(self, request: Request):
        body = self.__get_body_data(request)
        encrypted_body = BlockchainUtils.encrypt_data(body)
        signed_body = BlockchainUtils.sign(encrypted_body)

        try:
            transaction_body = {
                "signature": signed_body,
                "transaction_hash": encrypted_body.decode("utf-8"),
            }
            async with AsyncClient(base_url=self.base_url) as ac:
                response = await ac.post(
                    "/transactions",
                    json=transaction_body,
                )

                if response.status_code == 200:
                    open(self.transactions_log_file, "w").close() if not os.path.exists(
                        self.transactions_log_file
                    ) else None
                    with open(self.transactions_log_file, "ab") as file_obj:
                        file_obj.write(json.dumps(transaction_body).encode("utf-8"))
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
