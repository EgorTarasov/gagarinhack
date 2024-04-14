from asyncpg.pool import PoolConnectionProxy
from .schema import MlQuery, MlResponse
import asyncio
from . import crud
from uuid import UUID
from ml.client import MLClient
from utils.logging import log
from config import cfg


async def get_response():
    for i in range(10):
        yield f"msg: {i}"


async def save_chat(db: PoolConnectionProxy, user_id: int, chat_id: UUID) -> UUID:
    await crud.save_chat(db, user_id=user_id, chat_id=chat_id)
    return chat_id


async def inference(
    db: PoolConnectionProxy, ml_service: MLClient, chat_id: UUID, query: MlQuery
):
    response_txt = ""
    metadata = []
    q_id = await crud.save_query(db, chat_id, query.text)
    for msg in ml_service.stream_response(query.text):
        response_txt += msg.body
        yield MlResponse.model_validate(
            {"query_id": q_id, "text": msg.body, "metadata": []}
        )
    log.info(f"finished inference chat_id: {chat_id}")
    log.info(f"metadata:{' '.join(metadata)}")
    static_url = "/static/file/{filename}"

    yield MlResponse.model_validate(
        {
            "query_id": q_id,
            "text": "",
            "metadata": [filename for filename in msg.context.split(":")[1].split(";")],
            "last": True,
        }
    )

    await asyncio.create_task(
        crud.save_response(db, chat_id, q_id, response_txt, metadata)
    )
