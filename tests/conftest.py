import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.expression import text

from app.configs import ROOT_DIR
from app.database import Base
from app.dependencies import get_db
from app.domain.subjects.crud import create_subject
from app.domain.subjects.schemas import SubjectCreate
from app.domain.users.crud import create_user
from app.domain.users.schemas import UserCreate
from app.main import create_app
from app.security import create_access_token

DATABASE_URL = f"sqlite:///{ROOT_DIR / 'test.db'}"

engine = create_engine(DATABASE_URL, echo=True, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


@pytest.fixture(scope="function", autouse=True)
def run_around_tests():
    # Setup code
    with engine.connect() as conn:
        conn.execute(text("delete from subjects"))
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
def guest_client(app):
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
        form=UserCreate(
            username="tester",
            password="password",
        ),
    )


@pytest.fixture(scope="function")
def user2(session):
    return create_user(
        db=session,
        form=UserCreate(
            username="tester2",
            password="password",
        ),
    )


@pytest.fixture(scope="function")
def inactive_user(session):
    return create_user(
        db=session,
        form=UserCreate(
            username="inactiveuser",
            password="password",
        ),
    )


@pytest.fixture(scope="function")
def superuser(session, user):
    user.is_superuser = True
    session.commit()
    session.refresh(user)
    return user


@pytest.fixture(scope="function")
def inactive_superuser(session, superuser):
    superuser.is_active = False
    session.commit()
    session.refresh(superuser)
    return superuser


@pytest.fixture(scope="function")
def user_client(guest_client, user):
    access_token = create_access_token({"username": user.username})
    guest_client.headers = {"Authorization": "Bearer " + access_token}
    return guest_client


@pytest.fixture(scope="function")
def superuser_client(guest_client, superuser):
    access_token = create_access_token({"username": superuser.username})
    guest_client.headers = {"Authorization": "Bearer " + access_token}
    return guest_client


@pytest.fixture(scope="function")
def subject(session):
    return create_subject(
        db=session,
        form=SubjectCreate(
            name="수학",
        ),
    )
