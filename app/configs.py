import os
from pathlib import Path

import dotenv

ROOT_DIR = Path(__file__).parent.parent

dotenv.load_dotenv(ROOT_DIR / ".env")

SECRET_KEY = os.environ["SECRET_KEY"]
JWT_ALGORITHM = "HS256"
