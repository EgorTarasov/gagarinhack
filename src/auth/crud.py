from asyncpg.pool import PoolConnectionProxy
from .models import UserDao
from . import schema
from redis import Redis


async def get_hashed_password(
    db: PoolConnectionProxy, email: str
) -> tuple[int, str] | None:
    """Получение хэшированного пароля пользователя"""
    query = 'SELECT id, pswd FROM "users" WHERE email = $1'
    row = await db.fetchrow(query, email)
    if row is None:
        return None
    return (row["id"], row["pswd"])


async def get_by_email(db: PoolConnectionProxy, email: str) -> UserDao | None:
    """Получение пользователя по email"""
    query = 'SELECT id, email, first_name, last_name, created_at, updated_at FROM "users" WHERE email = $1'
    row = await db.fetchrow(query, email)
    if row is None:
        return None
    return UserDao(**row)


async def create_user(db: PoolConnectionProxy, user: schema.UserCreate) -> int | None:
    """Создание пользователя"""
    query = 'INSERT INTO "users" (email, pswd, first_name, last_name) VALUES ($1, $2, $3, $4) RETURNING id'
    try:
        new_id: int = await db.fetchval(
            query, user.email, user.password, user.first_name, user.last_name
        )
        return new_id
    except Exception as e:
        return None


async def save_reset_code(redis: Redis, email: str, code: str) -> None:
    """Сохранение кода восстановления пароля"""
    redis.set(name=code, value=email, ex=60 * 15)


async def get_reset_code(redis: Redis, code: str) -> str | None:
    """Получение кода восстановления пароля"""
    email = redis.get(code)
    if email is None:
        return None
    return email.decode()
