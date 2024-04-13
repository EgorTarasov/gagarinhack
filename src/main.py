from typing import AsyncGenerator

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from starlette.requests import Request

from config import cfg
from data import db

from auth.router import router as auth_router
from lifespan import InvalidDataException
from timetable.router import router as timetable_router
from news.router import router as news_router
from achievements.router import router as achievements_router

from chat.router import router as chat_router


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

    origins = [
        "http://localhost:9000",
        "https://gagarinhack.larek.tech",
        "http://localhost:5173",
    ]

    new_app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
    )

    new_app.include_router(auth_router)
    new_app.include_router(timetable_router)
    new_app.include_router(news_router)
    new_app.include_router(chat_router)
    new_app.include_router(achievements_router)

    return new_app


def exception_handler(request: Request, exc: Exception):
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


app = create_app()
app.add_exception_handler(InvalidDataException, exception_handler)