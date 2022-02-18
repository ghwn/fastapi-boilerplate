import databases
import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine

from app.configs import ROOT_DIR
from app.database import metadata
from app.dependencies import get_db
from app.domain.users.crud import create_user, patch_user
from app.domain.users.schemas import UserCreate, UserPatch
from app.main import create_app
from app.security import create_access_token

TEST_DATABASE_URL = f"sqlite+aiosqlite:///{ROOT_DIR / 'test.db'}"
database = databases.Database(TEST_DATABASE_URL)


@pytest_asyncio.fixture(autouse=True)
async def clear_db_before_each_test():
    engine = create_async_engine(TEST_DATABASE_URL, echo=True)
    async with engine.begin() as conn:
        await conn.run_sync(metadata.drop_all)
        await conn.run_sync(metadata.create_all)
        yield


@pytest.fixture(scope="session")
def app():
    async def override_get_db():
        async with database.transaction():
            yield database

    app = create_app()
    app.dependency_overrides[get_db] = override_get_db
    return app


@pytest_asyncio.fixture
async def guest_client(app):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest_asyncio.fixture
async def user():
    return await create_user(database, UserCreate(username="tester", password="password"))


@pytest_asyncio.fixture
async def user2():
    return await create_user(database, UserCreate(username="tester2", password="password"))


@pytest_asyncio.fixture
async def user_client(guest_client, user):
    access_token = create_access_token({"username": user.username})
    guest_client.headers = {"Authorization": "Bearer " + access_token}
    return guest_client


@pytest_asyncio.fixture
async def superuser(user):
    return await patch_user(database, user.username, UserPatch(is_superuser=True))


@pytest_asyncio.fixture
async def superuser_client(guest_client, superuser):
    access_token = create_access_token({"username": superuser.username})
    guest_client.headers = {"Authorization": "Bearer " + access_token}
    return guest_client


@pytest_asyncio.fixture
async def inactive_user(user):
    return await patch_user(database, user.username, UserPatch(is_active=False))


@pytest_asyncio.fixture
async def inactive_superuser(superuser):
    return await patch_user(database, superuser.username, UserPatch(is_active=False))
