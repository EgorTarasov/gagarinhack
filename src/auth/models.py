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
