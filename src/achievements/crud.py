from asyncpg.pool import PoolConnectionProxy

from achievements.schema import AchievementCreate, AchievementDto


async def get_by_id(db: PoolConnectionProxy, achievement_id: int, offset: int = 0, limit: int = 100) -> AchievementDto:
    """Получение достижения пользователя"""
    query = ('SELECT id, user_id, title, date, place, description, event_link, file_link, type '
             'FROM "achievements" WHERE id=$1')
    row = await db.fetchrow(query, achievement_id)
    return AchievementDto(**row)


async def get_all(db: PoolConnectionProxy, user_id: int, offset: int = 0, limit: int = 100) -> list[AchievementDto]:
    """Получение всех достижений пользователя"""
    query = ('SELECT id, user_id, title, date, place, description, event_link, file_link, type FROM "achievements" '
             'WHERE user_id=$1 ORDER BY date DESC OFFSET $2 LIMIT $3')
    rows = await db.fetch(query, user_id, offset, limit)
    return [AchievementDto(**row) for row in rows]


async def create(db: PoolConnectionProxy, achievement: AchievementCreate, static_name: str) -> int:
    """Добавление достижения"""
    query = ('INSERT INTO "achievements" (user_id, title, date, place, description, event_link, type, file_link) '
             'VALUES ($1, $2, $3, $4, $5, $6, $7, $8) RETURNING id')
    _id = await db.fetchval(query, achievement.user_id, achievement.title, achievement.date, achievement.place,
                            achievement.description, achievement.event_link, achievement.type, static_name)
    return _id
