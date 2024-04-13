import uuid

import minio
from asyncpg.pool import PoolConnectionProxy
from fastapi import UploadFile

from achievements import crud
from achievements.schema import AchievementCreate, AchievementDto
from config import cfg


async def upload_achievement(db_conn: PoolConnectionProxy,  minio_client: minio.Minio,
                             file: UploadFile, achievement: AchievementCreate) -> int:
    static_name = f"{uuid.uuid4()}.{file.filename.split('.')[-1]}"
    minio_client.put_object(bucket_name=cfg.s3_bucket, object_name=static_name,
                            data=file.file, length=file.size)
    return await crud.create(db_conn, achievement, static_name)


async def download_achievements(db_conn: PoolConnectionProxy, user_id: int,
                                offset: int = 0, limit: int = 100) -> list[AchievementDto]:
    return await crud.get_all(db_conn, user_id=user_id, offset=offset, limit=limit)


async def get_achievement(db_conn: PoolConnectionProxy, achievement_id: int) -> AchievementDto:
    return await crud.get_by_id(db_conn, achievement_id=achievement_id)