import minio
from fastapi import (
    APIRouter,
    Depends,
    UploadFile,
    File,
    Form,
    HTTPException,
)

from fastapi.responses import StreamingResponse, FileResponse
from asyncpg.pool import PoolConnectionProxy

from config import cfg

from typing import Annotated
from datetime import datetime

from data import get_connection, get_minio

from auth.dependency import get_current_user
from utils import UserTokenData

router = APIRouter(prefix="/static")


@router.get("/file/{filename}")
async def serve_file(
    filename: str,
    minio_client: minio.Minio = Depends(get_minio),
):
    """Serve a file from S3 storage."""
    try:
        data = minio_client.get_object(cfg.s3_bucket, filename)

        filename = "temp." + filename.split(".")[-1]
        with open(filename, "wb") as out_file:
            out_file.write(data.read())
    except minio.error.S3Error:
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(
        filename,
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@router.get("/download", response_class=StreamingResponse)
async def download_file(
    file_link: str,
    minio_client: minio.Minio = Depends(get_minio),
):
    """Скачивание файла из хранилища"""
    obj = minio_client.get_object(cfg.s3_bucket, file_link)
    return StreamingResponse(
        obj,
        media_type="application/octet-stream",
        headers={"Content-Disposition": f'attachment; filename="{file_link}"'},
    )
