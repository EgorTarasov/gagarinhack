from fastapi import APIRouter, Depends, Response, Query
from asyncpg.pool import PoolConnectionProxy

from . import service

from data import get_connection

router = APIRouter(prefix="/news", tags=["news"])


@router.post("/parse")
async def parse_news(
    db: PoolConnectionProxy = Depends(get_connection)
):
    """Синхронизация новостей с сайта (не потребуется после интеграции с LMS ITHub)"""
    return await service.parse_news(db)



@router.get("/")
async def get_news(
    db: PoolConnectionProxy = Depends(get_connection),
    offset: int = Query(0),
    limit: int = Query(100)
):
    """Подбор рекомендованных новостей с сайта"""
    return await service.get_news(db, offset, limit)
