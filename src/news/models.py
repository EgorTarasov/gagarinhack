from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class NewsDao:
    title: str
    created_at: datetime.date
    description: str
    image_link: str
    id: Optional[int] = None

