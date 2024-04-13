import uuid
from http.client import HTTPResponse

import minio
from fastapi import APIRouter, Depends, UploadFile, File
from fastapi.responses import FileResponse, StreamingResponse, Response
from asyncpg.pool import PoolConnectionProxy

from config import cfg
from . import service

from data import get_connection, get_minio
from .schema import AchievementCreate, AchievementDto

router = APIRouter(prefix="/achievements", tags=["achievements"])


@router.post("/upload", response_model=AchievementDto)
async def upload_achievement(
        achievement: AchievementCreate = Depends(),
        file: UploadFile = File(...),
        db: PoolConnectionProxy = Depends(get_connection),
        minio_client: minio.Minio = Depends(get_minio)
):
    """Загрузка достижения"""
    static_name = f"{uuid.uuid4()}.{file.filename.split('.')[-1]}"
    minio_client.put_object(bucket_name=cfg.s3_bucket, object_name=static_name,
                            data=file.file, length=file.size)
    achievement_id = await service.upload_achievement(db, achievement, static_name)
    achievement = await service.get_achievement(db, achievement_id)
    return achievement


@router.get("/get", response_model=list[AchievementDto])
async def get_achievements(
        user_id: int,
        db: PoolConnectionProxy = Depends(get_connection)
):
    """Получение достижений пользователя"""
    achievements = await service.download_achievements(db, user_id=user_id)
    return achievements


@router.get("/download", response_class=StreamingResponse)
async def download_achievement(
        file_link: str,
        minio_client: minio.Minio = Depends(get_minio)
):
    """Выгрузка файла-подтверждения достижения (например, диплома призёра)x"""
    obj = minio_client.get_object(cfg.s3_bucket, file_link)
    return StreamingResponse(
        obj,
        media_type='application/octet-stream',
        headers={'Content-Disposition': f'attachment; filename="{file_link}"'}
    )
