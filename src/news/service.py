from asyncpg.pool import PoolConnectionProxy

from news import crud, parsing


async def parse_news(db_conn: PoolConnectionProxy):
    await crud.insert_all(db_conn, parsing.parse_ithub_news())


async def get_news(db_conn: PoolConnectionProxy, offset: int, limit: int):
    return await crud.get_all(db_conn, offset=offset, limit=limit)
