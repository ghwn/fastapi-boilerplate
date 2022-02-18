from databases import Database
from fastapi.encoders import jsonable_encoder

from app.domain.models import users
from app.domain.users import schemas
from app.security import get_password_hash


async def create_user(db: Database, form: schemas.UserCreate):
    hashed_password = get_password_hash(form.password)
    created_user_id = await db.execute(
        users.insert().values(
            username=form.username,
            hashed_password=hashed_password,
            is_active=True,
            is_superuser=False,
        )
    )
    return await db.fetch_one(users.select().where(users.c.id == created_user_id))


async def get_user_list(db: Database, offset: int = 0, limit: int = 100, **kwargs):
    return await db.fetch_all(
        users.select().filter_by(**kwargs).order_by(users.c.id).offset(offset).limit(limit)
    )


async def get_user_by_username(db: Database, username: str):
    return await db.fetch_one(users.select().where(users.c.username == username))


async def update_user(db: Database, username: str, form: schemas.UserUpdate):
    params = jsonable_encoder(form, by_alias=False, exclude_unset=False, exclude={"password"})
    params["hashed_password"] = get_password_hash(form.password)
    await db.execute(users.update().where(users.c.username == username).values(**params))
    return await db.fetch_one(users.select().where(users.c.username == username))


async def patch_user(db: Database, username: str, form: schemas.UserPatch):
    params = jsonable_encoder(form, by_alias=False, exclude_unset=True, exclude={"password"})
    if form.password:
        params["hashed_password"] = get_password_hash(form.password)
    await db.execute(users.update().where(users.c.username == username).values(**params))
    return await db.fetch_one(users.select().where(users.c.username == username))


async def delete_user(db: Database, username: str):
    await db.execute(users.delete().where(users.c.username == username))
