import requests
from asyncpg.pool import PoolConnectionProxy
from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from config import cfg
from . import service
from data import get_connection

router = APIRouter(prefix="/timetable", tags=["timetable"])


@router.get("/get", response_class=FileResponse)
async def find(group: str) -> FileResponse:
    """Получить расписание"""
    return FileResponse("./tmp/бивт-21-16.ics", filename="бивт-21-16.ics", media_type='text/calendar')


@router.post("/update")
async def update(db_conn: PoolConnectionProxy = Depends(get_connection)):
    """Обновить расписание (не потребуется после интеграции с LMS ITHub)"""
    await service.upload_schedules(db_conn)


@router.get("/yandex_link", response_model=str)
async def get_yandex_link(to_address: str = "Москва, проспект Мира, 119с332",
                          from_address: str = "") -> str:
    """Получить ссылку на построение маршрута к корпусу с Yandex.Maps"""
    to_point = requests.get(f"https://geocode-maps.yandex.ru/1.x/?apikey={cfg.yandex_maps_key}&"
                            f"geocode={to_address}&format=json&results=1&sco=latlong")
    to_point = to_point.json()["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["Point"][
        "pos"].split()
    if not from_address:
        return f"https://yandex.ru/maps/?rtext=~{to_point[1]},{to_point[0]}"
    from_point = requests.get(f"https://geocode-maps.yandex.ru/1.x/?apikey={cfg.yandex_maps_key}&"
                              f"geocode={from_address}&format=json&results=1&sco=latlong")
    from_point = from_point.json()["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["Point"][
        "pos"].split()
    return f"https://yandex.ru/maps/?rtext={from_point[1]},{from_point[0]}~{to_point[1]},{to_point[0]}"
