import logging
from fastapi import APIRouter, Depends, Response
from fastapi.security import OAuth2PasswordRequestForm
from asyncpg.pool import PoolConnectionProxy
from redis import Redis

from auth import schema
from . import service

from data import get_connection, get_redis

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
async def login(
    db: PoolConnectionProxy = Depends(get_connection),
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    # TODO: valid err codes
    try:
        return await service.login(db, form_data.username, form_data.password)
    except ValueError as e:
        return {"detail": str(e)}


@router.post("/register")
async def register(
    user: schema.UserCreate,
    db: PoolConnectionProxy = Depends(get_connection),
):
    # TODO: valid err codes
    try:
        return await service.register(db, user)
    except ValueError as e:
        logging.error(e)
        return Response(status_code=400, content={"detail": str(e)})


@router.post("/login/vk")
async def login_vk(user_id: int):
    test_msg = "test notification"
    await service.send_notification(user_id, test_msg)
    return {"message": "Login VK"}


@router.post("/password-code")
async def password_code(
    email: str,
    db_conn: PoolConnectionProxy = Depends(get_connection),
    redis_client: Redis = Depends(get_redis),
):
    try:
        return await service.send_password_code(db_conn, redis_client, email)
    except ValueError as e:
        return {"detail": str(e)}


@router.get("/password-reset")
async def password_reset():
    return {"message": "Password Reset"}
