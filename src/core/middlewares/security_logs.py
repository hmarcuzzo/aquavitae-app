import json
from datetime import datetime

import cipher
from cryptography.fernet import Fernet
from httpx import AsyncClient
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp

from src.modules.infrastructure.auth.jwt_service import verify_token


class SecurityLogs(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp) -> None:
        super().__init__(app)
        self.base_url = "http://localhost:8000"
        self.route = "/api/v1/security-logs"

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        body = {
            "timestamp": datetime.now().timestamp(),
            "method": request.method,
            "path": request.url.path,
            "user_id": verify_token(request.headers["Authorization"].split(" ")[1], "user_id"),
        }

        key = Fernet.generate_key()
        cipher = Fernet(key)

        body_bytes = json.dumps(body).encode("utf-8")
        body_encrypted = cipher.encrypt(body_bytes)

        # async with AsyncClient(app=self.app, base_url=self.base_url) as ac:
        #     response = await ac.post(
        #         self.route,
        #         json=body_encrypted,
        #         headers={"Authorization": f"Bearer {'token'}"},
        #     )
        #
        # data = response.json()

        return await call_next(request)
