from fastapi import APIRouter, Depends
from asyncpg.pool import PoolConnectionProxy

from auth.dependency import get_current_user
from utils import UserTokenData
from . import service

from data import get_connection

router = APIRouter(prefix="/clubs", tags=["clubs"])


@router.get("/")
async def get_recommended_clubs(
    db: PoolConnectionProxy = Depends(get_connection),
    user: UserTokenData = Depends(get_current_user),
):
    """Подбор рекомендованных клубов с сайта"""
    return await service.get_recommended_clubs(db, user.user_id)
