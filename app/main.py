import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm.session import close_all_sessions

from app import configs
from app.database import engine
from app.domain.auth.routers import router as auth
from app.domain.users.routers import router as users
from app.exceptions import APIException


def create_app():
    logging.basicConfig(
        level=logging.DEBUG if configs.DEBUG else logging.INFO,
        format="%(levelname)s: %(processName)s %(threadName)s %(pathname)s::%(funcName)s"
        " L%(lineno)s -> %(message)s",
    )
    app_ = FastAPI()

    app_.include_router(
        users,
        prefix="/api/v1/users",
        tags=["Users"],
    )
    app_.include_router(
        auth,
        prefix="/auth",
        tags=["Auth"],
    )

    @app_.exception_handler(APIException)
    async def api_exception_handler(request: Request, exc: APIException):
        return JSONResponse(
            content={"detail": exc.detail},
            status_code=exc.status_code,
        )

    @app_.exception_handler(Exception)
    async def exception_handler(request: Request, exc: Exception):
        return JSONResponse(
            content={"detail": "Internal server error has been occurred."},
            status_code=500,
        )

    @app_.on_event("startup")
    async def startup():
        engine.connect()

    @app_.on_event("shutdown")
    async def shutdown():
        close_all_sessions()
        engine.dispose()

    return app_


app = create_app()
