from asyncpg.pool import PoolConnectionProxy
from redis import Redis

from worker import send_email_recovery_code, send_telegram_notification
from utils.password import PasswordManager
from utils.jwt import JWTEncoder
from . import schema
from . import crud


async def login(
    db_conn: PoolConnectionProxy,
    email: str,
    password: str,
) -> str:
    """Авторизация пользователя
    Returns:
        str: jwt token
    """
    data = await crud.get_hashed_password(db_conn, email)
    if data is None:
        raise ValueError("User not found")
    _id, hashed_password = data
    print(_id, hashed_password)
    print(password, hashed_password)
    if not PasswordManager.verify_password(password, hashed_password):
        raise ValueError("Invalid password")

    return JWTEncoder.create_access_token(_id)


async def register(db_conn: PoolConnectionProxy, user: schema.UserCreate) -> str:

    data = await crud.get_by_email(db_conn, user.email)

    if data is not None:
        raise ValueError("User already exists")

    user.password = PasswordManager.hash_password(user.password)

    new_id = await crud.create_user(db_conn, user)
    if new_id is None:
        raise ValueError("Error creating user")

    return JWTEncoder.create_access_token(new_id)


async def auth_vk(db_conn: PoolConnectionProxy) -> str:
    ...


async def send_password_code(db_conn: PoolConnectionProxy, redis, email: str) -> None:
    user = await crud.get_by_email(db_conn, email)
    if user is None:
        raise ValueError("User not found")
    code = PasswordManager.get_reset_code(email)
    await crud.save_reset_code(redis, email, code)

    send_email_recovery_code.delay(email, user.first_name, user.last_name, code)

    return None


async def send_notification(user_id: int, msg: str) -> None:
    send_telegram_notification.delay(user_id, msg)
