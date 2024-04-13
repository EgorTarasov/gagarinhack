from typing import Optional
from datetime import datetime

from pydantic import BaseModel


class ScheduleFiltersRequest(BaseModel):
    group_name: Optional[str] = None
    teacher_fio: Optional[str] = None
    room_id: Optional[str] = None
    start_date: Optional[datetime.date] = None
    end_date: Optional[datetime.date] = None

    # class Config:
    #     schema_extra = {
    #         "example": {
    #             "group_name": "БИВТ-21-17",
    #             "teacher_fio": "Ласурия Роберт Андреевич",
    #             "room_id": "Б-4",
    #             "start_date": "2023-06-12",
    #             "end_date": "2023-06-18",
    #         }
    #     }
