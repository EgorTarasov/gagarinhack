from pydantic import BaseModel, Field


class MlQuery(BaseModel):
    text: str = Field(...)


class MlResponse(BaseModel):
    query_id: int
    text: str
    metadata: list[str]
    last: bool = False
