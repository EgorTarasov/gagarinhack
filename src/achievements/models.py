from dataclasses import dataclass
from datetime import datetime

from fastapi import UploadFile, File


@dataclass
class AchievementDao:
    id: int
    user_id: int
    title: str
    date: datetime.date
    place: str
    description: str
    event_link: str
    file: UploadFile
