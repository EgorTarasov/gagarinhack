from typing import Optional
from pydantic import BaseModel, ConfigDict


class UserCreate(BaseModel):
    email: Optional[str]
    password: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]


class Token(BaseModel):
    access_token: str
    token_type: str = "Bearer"


class UserData(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    email: str
    first_name: str
    last_name: str
