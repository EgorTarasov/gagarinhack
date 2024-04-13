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
    # TODO: valid err codes
    try:
        return await service.parse_news(db)
    except ValueError as e:
        return {"detail": str(e)}


@router.get("/")
async def get_news(
    db: PoolConnectionProxy = Depends(get_connection),
    offset: int = Query(0),
    limit: int = Query(100)
):
    """Подбор рекомендованных новостей с сайта"""
    # TODO: valid err codes
    try:
        return await service.get_news(db, offset, limit)
    except ValueError as e:
        return {"detail": str(e)}