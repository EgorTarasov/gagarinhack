import datetime

from asyncpg.pool import PoolConnectionProxy
from .models import ChatDao, QueryDao, ResponseDao
from redis import Redis
from utils.logging import log
from uuid import UUID


async def save_chat(db: PoolConnectionProxy, user_id: int, chat_id: UUID):
    query = '''
INSERT INTO chat(id) values ($1);
'''
    await db.execute(query, chat_id)


async def save_query(db: PoolConnectionProxy, chat_id: UUID, text: str) -> int:
    query = '''
INSERT INTO query(fk_chat_id, body) values($1, $2) RETURNING ID;    
'''
    try:
        new_id = await db.fetchval(query, chat_id, text)
        return new_id
    except Exception as e:
        log.error(f"error in save_query: {e}")


async def save_response(db: PoolConnectionProxy, chat_id: UUID, query_id: int, response: str, metadata: list[str]) -> int:
    query = '''
INSERT INTO response(fk_chat_id, fk_query_id, body, metadata) VALUES ($1, $2, $3, $4) RETURNING id;
'''
    try:
        new_id = await db.fetchval(query, chat_id, query_id, response, metadata)
        return new_id
    except Exception as e:
        log.error(f"error in save_response {e}")


