from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.configs import DATABASE_URL, DEBUG

engine = create_engine(
    DATABASE_URL,
    echo=True if DEBUG else False,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else dict(),
)
SessionLocal = sessionmaker(bind=engine, autoflush=True, autocommit=False)


Base = declarative_base()
