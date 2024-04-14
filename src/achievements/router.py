import minio
from fastapi import APIRouter, Depends, UploadFile, File, Form
from fastapi.responses import StreamingResponse
from asyncpg.pool import PoolConnectionProxy

from config import cfg
from . import service
from typing import Annotated
from datetime import datetime

from data import get_connection, get_minio
from .schema import AchievementCreate, AchievementDto
from auth.dependency import get_current_user
from utils import UserTokenData

router = APIRouter(prefix="/achievements", tags=["achievements"])


@router.post("/upload", response_model=AchievementDto)
async def upload_achievement(
    # achievement: AchievementCreate = Depends(),
    title: Annotated[str, Form()],
    date: Annotated[str, Form()],
    place: Annotated[str, Form()],
    description: Annotated[str, Form()],
    type: Annotated[str, Form()],
    event_link: Annotated[str, Form()],
    file: UploadFile = File(...),
    db: PoolConnectionProxy = Depends(get_connection),
    minio_client: minio.Minio = Depends(get_minio),
    token_data: UserTokenData = Depends(get_current_user),
):
    """Загрузка достижения"""
    achievement = AchievementCreate.model_validate(
        {
            "user_id": token_data.user_id,
            "title": title,
            # "date": datetime.now().date,
            "place": place,
            "description": description,
            "type": type,
            "event_link": event_link,
        }
    )
    achievement_id = await service.upload_achievement(
        db, minio_client, file, achievement
    )
    achievement = await service.get_achievement(db, achievement_id)
    return achievement


@router.get("/get", response_model=list[AchievementDto])
async def get_achievements(
    db: PoolConnectionProxy = Depends(get_connection),
    token_data: UserTokenData = Depends(get_current_user),
):
    """Получение достижений пользователя"""
    achievements = await service.download_achievements(db, user_id=token_data.user_id)
    return achievements


@router.get("/download", response_class=StreamingResponse)
async def download_achievement(
    file_link: str,
    minio_client: minio.Minio = Depends(get_minio),
    _=Depends(get_current_user),
):
    """Выгрузка файла-подтверждения достижения (например, диплома призёра)"""
    obj = minio_client.get_object(cfg.s3_bucket, file_link)
    return StreamingResponse(
        obj,
        media_type="application/octet-stream",
        headers={"Content-Disposition": f'attachment; filename="{file_link}"'},
    )


@router.delete("/delete")
async def delete_achievement(
    achievement_id: int,
    db: PoolConnectionProxy = Depends(get_connection),
    _=Depends(get_current_user),
):
    """Удаление достижения"""
    await service.delete_achievement(db, achievement_id)
