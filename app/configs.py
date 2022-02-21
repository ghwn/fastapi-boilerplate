import os
from pathlib import Path

import dotenv

ROOT_DIR = Path(__file__).parent.parent

dotenv.load_dotenv(ROOT_DIR / ".env")

DEBUG = bool(int(os.getenv("DEBUG", default="1")))


# -------------------------------------------------------------------------------------------------
# Security
SECRET_KEY = os.environ["SECRET_KEY"]
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRATION_TIME = 900


# -------------------------------------------------------------------------------------------------
# Database
DATABASE_URL = os.getenv("DATABASE_URL") or f"sqlite:///{ROOT_DIR / 'app.db'}"

# https://docs.sqlalchemy.org/en/14/core/engines.html#sqlalchemy.create_engine
DATABASE_ECHO = DEBUG
DATABASE_ECHO_POOL = DEBUG
DATABASE_MAX_OVERFLOW = 10
DATABASE_POOL_PRE_PING = True
DATABASE_POOL_SIZE = 5
DATABASE_POOL_RECYCLE = ACCESS_TOKEN_EXPIRATION_TIME
DATABASE_POOL_TIMEOUT = 30
DATABASE_POOL_USE_LIFO = False
DATABASE_QUERY_CACHE_SIZE = 500
