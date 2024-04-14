import asyncio

from asyncpg.pool import PoolConnectionProxy
from worker import send_email_recovery_code
from config import cfg
import requests
from utils.password import PasswordManager
from utils.jwt import JWTEncoder
from utils.logging import log
from typing import Any
from datetime import datetime
from . import schema
from . import models
from . import crud
from .exeptions import UserNotFoundException


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

    if not PasswordManager.verify_password(password, hashed_password):
        raise ValueError("Invalid password")

    return JWTEncoder.create_access_token(_id)


async def register(db_conn: PoolConnectionProxy, user: schema.UserCreate) -> str:
    if user.email is None:
        raise ValueError("empty email")
    data = await crud.get_by_email(db_conn, user.email)

    if data is not None:
        raise UserNotFoundException(
            f"Пользователь с почтой {user.email} уже существует"
        )

    user.password = PasswordManager.hash_password(user.password)

    new_id = await crud.create_user(db_conn, user)
    if new_id is None:
        raise ValueError("Error creating user")

    return JWTEncoder.create_access_token(new_id)


async def send_password_code(db_conn: PoolConnectionProxy, redis, email: str) -> None:
    user = await crud.get_by_email(db_conn, email)
    if user is None:
        raise ValueError("User not found")
    code = PasswordManager.get_reset_code(email)
    await crud.save_reset_code(redis, email, code)

    send_email_recovery_code.delay(email, user.first_name, user.last_name, code)

    return None


async def send_notification(user_id: int, msg: str) -> None:
    print("sending telegram notification to user", user_id, msg)
    # send_telegram_notification.delay(user_id, msg)


async def auth_vk(db_conn: PoolConnectionProxy, code: str) -> str:
    # Checks vk auth
    url = cfg.vk_token_url.format(
        client_id=cfg.vk_client_id,
        vk_secure_token=cfg.vk_secure_token,
        redirect_uri=cfg.vk_redirect_uri,
        code=code,
    )
    response = requests.get(url)

    if response.status_code != 200:
        log.info(response.status_code)
        log.info(response.json())
        raise Exception("unathorized")

    # Gets user data from vk

    access_token = response.json()["access_token"]
    user_id = int(response.json()["user_id"])

    user_data = await crud.get_vk_user(db_conn, user_id)
    # If we don't have data read it from vk
    if user_data is None:
        response = requests.get(
            cfg.vk_base_url + "/users.get",
            headers={"Authorization": f"Bearer {access_token}"},
            params={"fields": "photo_200, sex, city, bdate, schools", "v": "5.199"},
        )

        user_info: dict[str, Any] = response.json()["response"][0]

        if "bdate" in user_info.keys():
            d, m, y = map(int, user_info["bdate"].split("."))  # 10.6.2003
            bdate = datetime(y, m, d)
        else:
            bdate = datetime(2000, 1, 1)

        if "city" in user_info.keys():
            city = user_info["city"]["title"]
        else:
            city = "Не указан"

        if "sex" in user_info.keys():
            """
            1 — женский;
            2 — мужской;
            0 — пол не указан.
            """
            if user_info["sex"] == 1:
                sex = "женский"
            elif user_info["sex"] == 2:
                sex = "мужской"
            else:
                sex = "пол не указан"
        else:
            sex = "пол не указан"
        user_data = models.VkUserDao(
            id=user_id,
            first_name=user_info["first_name"],
            last_name=user_info["last_name"],
            photo_url=user_info["photo_200"],
            created_at=datetime.now(),
            updated_at=datetime.now(),
            sex=sex,
            bdate=bdate,
            city=city,
        )
        new_id = await crud.create_vk_user(db_conn, user_data)
        if new_id is None:
            # что-то пошло не так(
            raise Exception("ошибка при создании профиля")

    # на данный момент в user_data точно будут все нужные данные
    await asyncio.create_task(parse_vk(db_conn, access_token, user_data))

    return JWTEncoder.create_access_token(user_id)


async def parse_vk(
    db: PoolConnectionProxy, access_token: str, user_data: models.VkUserDao
):
    # TODO: add embedings to groups
    response = requests.get(
        cfg.vk_base_url + "/groups.get",
        headers={"Authorization": f"Bearer {access_token}"},
        params={"v": "5.199"},
    )

    old_groups = await crud.select_groups(db, response.json()["response"]["items"])

    db_groups: dict[int, models.VkGroupDao] = {gr.id: gr for gr in old_groups}

    response = requests.get(
        cfg.vk_base_url + "/groups.getById",
        headers={"Authorization": f"Bearer {cfg.vk_service_token}"},
        params={
            "group_ids": ",".join(map(str, response.json()["response"]["items"])),
            "fields": "photo_200,description",
            "v": "5.199",
        },
    )

    new_groups: list[models.VkGroupDao] = []

    for group_info in response.json()["response"]["groups"]:
        group_id = int(group_info["id"])
        if group_id in db_groups.keys():
            db_groups[group_id].name = group_info["name"]
            db_groups[group_id].description = group_info["description"]
            db_groups[group_id].type = group_info["type"]

        else:
            try:
                new_groups.append(
                    models.VkGroupDao(
                        id=group_info["id"],
                        name=group_info["name"],
                        screen_name=group_info["screen_name"],
                        description=(
                            group_info["description"]
                            if "description" in group_info.keys()
                            else ""
                        ),
                        type=group_info["type"],
                        photo_200=group_info["photo_200"],
                        created_at=datetime.now(),
                        updated_at=datetime.now(),
                    )
                )
            except Exception as e:
                log.error(f"failed to create VkGroupDao: {e}")
                log.error(group_info)

    await asyncio.create_task(crud.create_vk_groups(db, new_groups))
    await asyncio.create_task(
        crud.assign_groups_to_user(
            db, user_data.id, groups_ids=[obj.id for obj in new_groups]
        )
    )
