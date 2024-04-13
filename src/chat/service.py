from asyncpg.pool import PoolConnectionProxy
from .schema import MlQuery, MlResponse
import asyncio
from . import crud
from uuid import UUID


async def get_response():
    for i in range(10):
        yield f"msg: {i}"


async def save_chat(db: PoolConnectionProxy, user_id: int, chat_id: UUID) -> UUID:
    await crud.save_chat(db, user_id=user_id, chat_id=chat_id)
    return chat_id


async def inference(db: PoolConnectionProxy, chat_id: UUID, query: MlQuery):
    response_txt = ""
    metadata = []
    q_id = await crud.save_query(db, chat_id, query.text)
    async for msg in get_response():
        # TODO: connect to ml service and get stream response
        response_txt += msg
        yield MlResponse.model_validate({"query_id": q_id, "text":msg, "metadata": ["meta1"]})
    yield MlResponse.model_validate({"query_id": q_id, "text": "", "metadata": [], "last": True})

    await asyncio.create_task(crud.save_response(db, chat_id, q_id, response_txt, metadata))
