import uvicorn
from fastapi import FastAPI
from sqlalchemy.orm.session import close_all_sessions

from app.database import Base, engine
from app.domain.users.routers import router as users


def create_app():
    app_ = FastAPI()
    app_.include_router(users, prefix="/api/v1/users", tags=["Users"])
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
