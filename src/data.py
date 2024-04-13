import logging
import asyncpg as pg
from typing import Any, AsyncGenerator, Generator
import redis
import minio
from asyncpg.pool import PoolConnectionProxy
from config import Config, cfg


class Database:

    def __init__(self, cfg: Config, retry: int = 3):
        self.dsn = cfg.build_postgres_dsn
        self.retry = retry

    async def connect(self):

        pool = await pg.create_pool(dsn=self.dsn)
        if pool is None:
            for _ in range(self.retry):
                pool = await pg.create_pool(dsn=self.dsn)
                if pool is not None:
                    break
        if pool is None:
            raise Exception(f"can't connect to db in {self.retry} retries")
        self.pool = pool

    async def disconnect(self):
        await self.pool.close()


db = Database(cfg)
redis_client = redis.Redis(
    host=cfg.redis_host,
    port=cfg.redis_port,
)

minio_client = minio.Minio(
    cfg.s3_endpoint,
    access_key=cfg.aws_access_key_id,
    secret_key=cfg.aws_secret_access_key,
)


async def get_redis() -> AsyncGenerator[redis.Redis, None]:
    yield redis_client


async def get_minio() -> AsyncGenerator[minio.Minio, None]:
    yield minio_client


async def get_connection() -> AsyncGenerator[PoolConnectionProxy, None]:
    logging.debug("Getting connection")
    async with db.pool.acquire() as conn:
        yield conn
    logging.debug("Releasing connection")
