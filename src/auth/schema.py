from typing import Optional
from pydantic import BaseModel


class UserCreate(BaseModel):
    email: Optional[str]
    password: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]


class Token(BaseModel):
    access_token: str
    token_type: str = "Bearer"


