from pydantic import BaseModel, Field
import typing as tp


class MlQuery(BaseModel):
    text: str = Field(...)


SENDER = tp.Literal["assistant", "user"]


class MlResponse(BaseModel):
    query_id: int
    text: str
    metadata: list[str]
    last: bool = False
    sender: SENDER = "assistant"
