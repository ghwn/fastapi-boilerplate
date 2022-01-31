import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.expression import text

from app.configs import ROOT_DIR
from app.database import Base
from app.dependencies import get_db
from app.domain.users.crud import create_user
from app.domain.users.schemas import UserCreate
from app.main import create_app

SQLALCHEMY_DATABASE_URL = f"sqlite:///{ROOT_DIR / 'test.db'}"

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


@pytest.fixture(scope="function", autouse=True)
def run_around_tests():
    # Setup code
    with engine.connect() as conn:
        conn.execute(text("delete from users"))
    yield
    # Teardown code


@pytest.fixture(scope="session")
def app():
    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    my_app = create_app()
    my_app.dependency_overrides[get_db] = override_get_db
    return my_app


@pytest.fixture(scope="session")
def client(app):
    return TestClient(app=app)


@pytest.fixture(scope="session")
def session():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def user(session):
    return create_user(
        db=session,
        data=UserCreate(
            username="tester",
            password="password",
        ),
    )
