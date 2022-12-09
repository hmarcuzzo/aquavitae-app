from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp

from src.modules.blockchain.blockchain_service import BlockchainService


class SecurityLogs(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp) -> None:
        super().__init__(app)
        self.blockchain_service = BlockchainService()

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        await self.blockchain_service.send_new_block(request)

        return await call_next(request)
