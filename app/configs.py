import os
from pathlib import Path

import dotenv

ROOT_DIR = Path(__file__).parent.parent

dotenv.load_dotenv(ROOT_DIR / ".env")

DATABASE_URL = os.getenv("DATABASE_URL") or f"sqlite:///{ROOT_DIR / 'app.db'}"
DEBUG = bool(int(os.getenv("DEBUG", default="1")))

SECRET_KEY = os.environ["SECRET_KEY"]
JWT_ALGORITHM = "HS256"
