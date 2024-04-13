from typing import Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class UserCreate:
    email: str
    password: str
    first_name: str
    last_name: str


@dataclass
class UserDao:
    id: int
    email: str
    first_name: str
    last_name: str
    created_at: datetime
    updated_at: datetime


@dataclass
class RecoveryCode:
    email: str
    code: str
    created_at: datetime


@dataclass
class VkUserDao:
    id: int
    first_name: Optional[str]
    last_name: Optional[str]
    photo_url: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    bdate: Optional[datetime]
    sex: Optional[str]
    city: Optional[str]


@dataclass
class VkGroupDao:
    id: int
    name: str
    screen_name: str
    description: str
    type: str
    photo_200: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
