import logging
from typing import AsyncGenerator
from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager


from config import cfg
from data import db, get_connection
from worker import celery_client
from auth.router import router as auth_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    if db is None:
        raise ValueError("Database is not initialized")
    await db.connect()
    yield
    await db.pool.close()


def create_app() -> FastAPI:
    new_app = FastAPI(
        title=cfg.app_name,
        description=cfg.app_desc,
        version=cfg.app_version,
        debug=cfg.debug,
        lifespan=lifespan,
    )
    logging.basicConfig(level=logging.DEBUG)

    new_app.include_router(auth_router)
    return new_app


app = create_app()
