from dataclasses import dataclass
from uuid import UUID
from datetime import datetime


@dataclass
class ChatDao:
    id: UUID
    user_id: int
    created_at: datetime


@dataclass
class QueryDao:
    id: int
    chat_id: UUID
    body: str
    created_at: datetime


@dataclass
class ResponseDao:
    id: int
    chat_id: UUID
    query_id: int
    response: str
    metadata: list[str]
    created_at: datetime

