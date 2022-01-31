from fastapi.logger import logger
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response

from app.exceptions import APIException


class ExceptionHandlingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        try:
            response = await call_next(request)
            return response
        except APIException as e:
            # logger.error(e.detail, exc_info=e)
            return JSONResponse(
                content={"detail": e.detail},
                status_code=e.status_code,
            )
        except Exception as e:
            logger.error("Unexpected error has been occurred.", exc_info=e)
            return JSONResponse(
                content={"detail": "Sorry, an internal server error has been occurred."},
                status_code=500,
            )