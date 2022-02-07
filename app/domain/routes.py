from typing import Any, Callable, Coroutine
from uuid import uuid4

from fastapi import Request, Response
from fastapi.logger import logger
from fastapi.routing import APIRoute


class APIRequestResponseLoggingRoute(APIRoute):
    def get_route_handler(self) -> Callable[[Request], Coroutine[Any, Any, Response]]:
        super_route_handler = super().get_route_handler()

        async def handle(request: Request) -> Response:
            request_id = uuid4().hex[:8]

            request_body = await request.body()

            if request.headers.get("Content-Type") not in ["application/json"]:
                request_body = "skip..."

            logger.info(
                "request %s | REQUEST_BODY = %s | %s",
                request_id,
                request_body,
                request.headers,
            )

            response: Response = await super_route_handler(request)
            response_body = response.body

            if request.headers.get("Content-Type") not in ["application/json"]:
                response_body = "skip..."

            logger.info(
                "request %s | STATUS_CODE = %s | RESPONSE_BODY = %s | %s",
                request_id,
                response.status_code,
                response_body,
                response.headers,
            )

            return response

        return handle
