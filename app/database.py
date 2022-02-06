from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from app import configs


def make_engine_args():
    args = {
        "echo": configs.DATABASE_ECHO,
        "echo_pool": configs.DATABASE_ECHO_POOL,
        "pool_pre_ping": configs.DATABASE_POOL_PRE_PING,
        "pool_recycle": configs.DATABASE_POOL_RECYCLE,
        "query_cache_size": configs.DATABASE_QUERY_CACHE_SIZE,
    }

    if configs.DATABASE_URL.startswith("sqlite"):
        args["connect_args"] = {"check_same_thread": False}
    else:
        args["max_overflow"] = configs.DATABASE_MAX_OVERFLOW
        args["pool_size"] = configs.DATABASE_POOL_SIZE
        args["pool_timeout"] = configs.DATABASE_POOL_TIMEOUT
        args["pool_use_lifo"] = configs.DATABASE_POOL_USE_LIFO

    return args


engine = create_engine(configs.DATABASE_URL, **make_engine_args())
SessionLocal = scoped_session(sessionmaker(bind=engine, autoflush=True, autocommit=False))

Base = declarative_base()
