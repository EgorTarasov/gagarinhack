from dataclasses import dataclass
from datetime import datetime


@dataclass
class Lesson:
    id: int
    title: str
    weekday: int
    arrangement: int
    odd_even_week: int
    type: str
    lesson_time: datetime
