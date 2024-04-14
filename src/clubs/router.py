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
    res = await service.get_recommended_clubs(db, user.user_id)
    print(res)
    return [
        {
            "title": "Математический клуб",
            "description": "Математика — это так интересно, что изучать её можно и нужно дополнительно! Любишь математику? Приходи! Ведёт занятия преподаватель по математике Алексей Зарали.",
            "contact": "https://t.me/tarasov_egor",
        },
        {
            "title": "Клуб косплея",
            "description": "Многие сейчас увлекаются компьютерными играми и аниме. Оружия и костюмы персонажей хочется подержать в руках или примерить на себе. Вместо того, чтобы покупать готовый реквизит в интернет-магазинах, его можно сделать самому. Основатель клуба Алексей готов помочь каждому в этом непростом, но очень интересном деле.",
            "contact": "https://t.me/lissey_t",
        },
    ]
