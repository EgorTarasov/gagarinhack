from contextlib import asynccontextmanager
from fastapi import FastAPI
from data import Database
from config import cfg


@asynccontextmanager
async def lifespan(app: FastAPI):
    db = Database(cfg)
    await db.connect()
    app.state.db = db
    yield
    await db.pool.close()
