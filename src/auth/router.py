import logging
from fastapi import APIRouter, Depends, Query, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from asyncpg.pool import PoolConnectionProxy
from redis import Redis

from utils import UserTokenData
from . import schema, crud, service

from data import get_connection, get_redis
from .dependency import get_current_user
from .models import UserDao

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=schema.Token)
async def login(
    db: PoolConnectionProxy = Depends(get_connection),
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    """Вход по почте и паролю (не потребуется после интеграции с LMS ITHub)"""
    token = await service.login(db, form_data.username, form_data.password)
    return schema.Token(access_token=token)


@router.post("/register", response_model=schema.Token)
async def register(
    user: schema.UserCreate,
    db: PoolConnectionProxy = Depends(get_connection),
):
    """Регистрация пользователя (не потребуется после интеграции с LMS ITHub)"""
    token = await service.register(db, user)
    return schema.Token(access_token=token)


@router.post("/password-code")
async def password_code(
    email: str,
    db_conn: PoolConnectionProxy = Depends(get_connection),
    redis_client: Redis = Depends(get_redis),
):
    """Восстановление пароля по почте"""
    return await service.send_password_code(db_conn, redis_client, email)


@router.get("/password-reset")
async def password_reset():
    """Сброс пароля"""
    return {"message": "Password Reset"}


@router.post("/vk")
async def auth_vk(
    code: str = Query(..., description="код авторизации"),
    db_conn: PoolConnectionProxy = Depends(get_connection),
):
    """Авторизация ВК по коду подтверждения"""
    token = await service.auth_vk(db_conn, code)
    return schema.Token(access_token=token)


@router.get("/me", response_model=UserDao)
async def get_me(
    db_conn: PoolConnectionProxy = Depends(get_connection),
    user: UserTokenData = Depends(get_current_user),
):
    """Получение текущего пользователя"""
    user = await crud.get_by_id(db_conn, user.user_id)
    return user
