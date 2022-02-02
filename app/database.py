from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.configs import ROOT_DIR

SQLALCHEMY_DATABASE_URL = f"sqlite:///{ROOT_DIR / 'app.db'}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True,
    connect_args={"check_same_thread": False},
)
SessionLocal = sessionmaker(bind=engine, autoflush=True, autocommit=False)


Base = declarative_base()
