from asyncpg.pool import PoolConnectionProxy

from achievements import crud
from achievements.schema import AchievementCreate, AchievementDto


async def upload_achievement(db_conn: PoolConnectionProxy, achievement: AchievementCreate,
                             static_name: str) -> int:
    return await crud.create(db_conn, achievement, static_name)


async def download_achievements(db_conn: PoolConnectionProxy, user_id: int,
                                offset: int = 0, limit: int = 100) -> list[AchievementDto]:
    return await crud.get_all(db_conn, user_id=user_id, offset=offset, limit=limit)


async def get_achievement(db_conn: PoolConnectionProxy, achievement_id: int) -> AchievementDto:
    return await crud.get_by_id(db_conn, achievement_id=achievement_id)