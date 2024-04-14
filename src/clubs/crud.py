from asyncpg import Record
from asyncpg.pool import PoolConnectionProxy
from .models import NewsDao
from utils.logging import log


async def get_all(
    db: PoolConnectionProxy, offset: int = 0, limit: int = 100
) -> list[NewsDao]:
    """Получение всех новостей"""
    query = (
        'SELECT id, title, created_at, description, image_link FROM "news" ORDER BY created_at '
        "DESC OFFSET $1 LIMIT $2"
    )
    rows = await db.fetch(query, offset, limit)
    return [NewsDao(**row) for row in rows]


async def insert_all(db: PoolConnectionProxy, all_news: list[NewsDao]):
    """Вставка всех новостей"""
    for news in all_news:
        query = 'INSERT INTO "news" (id, title, created_at, description, image_link) VALUES ($1, $2, $3, $4, $5) RETURNING id'
        _id = await db.fetchval(
            query,
            news.id,
            news.title,
            news.created_at,
            news.description,
            news.image_link,
        )


async def select_user_groups(db: PoolConnectionProxy, user_id: int) -> list[int]:
    query = """SELECT vk_group_id from user_group_association where vk_user_id = $1;"""
    try:
        results: list[Record] = await db.fetch(query, user_id)
        return [record["vk_group_id"] for record in results]
    except Exception as e:
        log.error("err in select groups")
        log.error(str(e))
        return []
