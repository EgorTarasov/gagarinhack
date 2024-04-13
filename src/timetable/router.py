import logging
from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from . import service
from data import get_connection

from asyncpg.pool import PoolConnectionProxy


router = APIRouter(prefix="/timetable", tags=["timetable"])


@router.get("/get", response_class=FileResponse)
async def find(group: str) -> FileResponse:
    return FileResponse("./tmp/бивт-21-16.ics", filename="бивт-21-16.ics", media_type='text/calendar')


@router.post("/update")
async def update(db_conn: PoolConnectionProxy = Depends(get_connection)):
    await service.upload_schedules(db_conn)