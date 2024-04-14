from asyncpg.pool import PoolConnectionProxy
from .models import UserDao, VkUserDao, VkGroupDao
from . import schema
from redis import Redis
from utils.logging import log


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


async def get_by_id(db: PoolConnectionProxy, user_id: int) -> UserDao | None:
    """Получение пользователя по email"""
    query = 'SELECT id, email, first_name, last_name, created_at, updated_at FROM "users" WHERE id = $1'
    row = await db.fetchrow(query, user_id)
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
        log.error(str(e))
        return None


async def get_vk_user(db: PoolConnectionProxy, user_id: int) -> None | VkUserDao:
    query = """
SELECT id, first_name, last_name, photo_url, created_at, updated_at, bdate, sex, city 
from vk_users
where deleted = false and id = $1;
"""
    row = await db.fetchrow(query, user_id)
    if row is None:
        return None
    return VkUserDao(**row)


async def create_vk_user(db: PoolConnectionProxy, user_data: VkUserDao) -> int | None:
    query = """
INSERT INTO vk_users(id, first_name, last_name, photo_url, bdate, sex, city) 
values 
    ($1, $2, $3, $4, $5, $6, $7)
returning id;
    """
    try:
        new_id: int = await db.fetchval(
            query,
            user_data.id,
            user_data.first_name,
            user_data.last_name,
            user_data.photo_url,
            user_data.bdate,
            user_data.sex,
            user_data.city,
        )
        await create_user(
            db,
            schema.UserCreate(
                email=f"{user_data.id}@vk.ru",
                password="",
                first_name=user_data.first_name,
                last_name=user_data.last_name,
            ),
        )
        return new_id
    except Exception as e:
        log.error(str(e))
        return None


async def create_vk_group(db: PoolConnectionProxy, group: VkGroupDao) -> int | None:
    query = """
INSERT INTO vk_groups(id, name, description, type, photo_200)
values 
    ($1, $2, $3, $4, $5)
returning id;  
"""
    try:
        new_id: int = await db.fetchval(
            query,
            group.id,
            group.name,
            group.description,
            group.type,
            group.photo_200,
        )
        return new_id
    except Exception as e:
        log.error(f"err in create_vk_group: {e}")
        return None


async def create_vk_groups(db: PoolConnectionProxy, groups: list[VkGroupDao]) -> None:
    records = [
        (
            obj.id,
            obj.name,
            obj.type,
            obj.photo_200,
            obj.description,
            obj.screen_name,
        )
        for obj in groups
    ]
    try:
        await db.copy_records_to_table(
            table_name="vk_groups",
            records=records,
            columns=["id", "name", "type", "photo_200", "description", "screen_name"],
        )
    except Exception as e:
        log.error(f"err in create_vk_groups: {e}")
        return None


async def assign_group_to_user(
    db: PoolConnectionProxy, user_id: int, group_id: int
) -> None:
    query = """
INSERT INTO user_group_association(vk_user_id, vk_group_id) values ($1, $2);
"""
    try:
        await db.execute(query, user_id, group_id)
    except Exception as e:
        log.error(f"err in assign group: {e}")
        return None


async def assign_groups_to_user(
    db: PoolConnectionProxy, user_id: int, groups_ids: list[int]
) -> None:
    records = [(user_id, gr_id) for gr_id in groups_ids]
    try:
        await db.copy_records_to_table(
            table_name="user_group_association",
            records=records,
            columns=["vk_user_id", "vk_group_id"],
        )
    except Exception as e:
        log.error(f"err in assign_groups_to_user: {e}")

        return None


async def select_groups(
    db: PoolConnectionProxy, ids: list[int]
) -> list[VkGroupDao] | None:
    if len(ids) == 0:
        return []
    query = """
SELECT id, name, description, screen_name, type, photo_200, created_at, updated_at
FROM vk_groups
WHERE id = ANY($1::integer[]);
"""
    try:
        results = await db.fetch(query, ids)
        return [VkGroupDao(**row) for row in results]
    except Exception as e:
        log.error("err in select groups")
        log.error(str(e))
        return []


async def save_reset_code(redis: Redis, email: str, code: str) -> None:
    """Сохранение кода восстановления пароля"""
    redis.set(name=code, value=email, ex=60 * 15)


async def get_reset_code(redis: Redis, code: str) -> str | None:
    """Получение кода восстановления пароля"""
    email = redis.get(code)
    if email is None:
        return None
    return email.decode()
