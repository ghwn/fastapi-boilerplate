import databases
from sqlalchemy import MetaData

from app import configs

database = databases.Database(configs.DATABASE_URL)
metadata = MetaData()
