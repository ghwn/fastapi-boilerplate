import uvicorn
from fastapi import Depends, FastAPI
from sqlalchemy.orm.session import close_all_sessions

from app.database import Base, engine
from app.dependencies import get_bearer_token
from app.domain.auth.routers import router as auth
from app.domain.subjects.routers import router as subjects
from app.domain.users.routers import router as users
from app.middlewares import ExceptionHandlingMiddleware


def create_app():
    app_ = FastAPI()
    app_.include_router(
        users,
        prefix="/api/v1/users",
        tags=["Users"],
        dependencies=[Depends(get_bearer_token)],
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
        dependencies=[Depends(get_bearer_token)],
    )
    app_.add_middleware(ExceptionHandlingMiddleware)
    return app_


app = create_app()


@app.on_event("startup")
async def startup():
    Base.metadata.create_all(bind=engine)


@app.on_event("shutdown")
async def shutdown():
    close_all_sessions()
    engine.dispose()


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
