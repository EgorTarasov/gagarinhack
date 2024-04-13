import datetime

from fastapi import UploadFile
from pydantic import BaseModel, Field, ConfigDict


class AchievementCreate(BaseModel):
    user_id: int = Field(1)
    title: str = Field("Gagarin Hack")
    date: datetime.date = Field(datetime.datetime.today().date())
    place: str = Field("Moscow")
    description: str = Field("...")
    event_link: str = Field("https://ithub.ru/")


class AchievementDto(AchievementCreate):
    id: int
    file_link: str
    model_config = ConfigDict(from_attributes=True)



