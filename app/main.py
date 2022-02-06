import logging

from fastapi import Depends, FastAPI
from sqlalchemy.orm.session import close_all_sessions

from app import configs
from app.database import engine
from app.dependencies import get_current_user
from app.domain.auth.routers import router as auth
from app.domain.subjects.routers import router as subjects
from app.domain.users.routers import router as users
from app.middlewares import ExceptionHandlingMiddleware


def create_app():
    logging.basicConfig(
        level=logging.DEBUG if configs.DEBUG else logging.INFO,
        format="%(levelname)s: %(processName)s %(threadName)s %(pathname)s::%(funcName)s"
        " L%(lineno)s -> %(message)s",
    )
    app_ = FastAPI()
    app_.add_middleware(ExceptionHandlingMiddleware)
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
    app_.include_router(
        subjects,
        prefix="/api/v1/subjects",
        tags=["Subjects"],
        dependencies=[Depends(get_current_user)],
    )
    return app_


app = create_app()


@app.on_event("startup")
async def startup():
    engine.connect()


@app.on_event("shutdown")
async def shutdown():
    close_all_sessions()
    engine.dispose()
