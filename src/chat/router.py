import uuid

from fastapi import APIRouter, WebSocket, Depends
from fastapi.responses import HTMLResponse
from data import get_connection
from asyncpg.pool import PoolConnectionProxy
from ml import client
from . import service
from .schema import  MlQuery, MlResponse

router = APIRouter(prefix="/chat", tags=["chat"])


@router.get("/")
async def get():
    """Стартовое сообщение диалога"""
    with open("./templates/chat.html") as file:
        html = file.read()
    return HTMLResponse(html)


# TODO: auth for websocket
@router.websocket("/ws/{chat_id}")
async def websocket_endpoint(
        websocket: WebSocket,
        chat_id: uuid.UUID,
        ml_client: client.MLClient = Depends(client.get_ml_service),
        db: PoolConnectionProxy = Depends(get_connection),
):
    # TODO: fixme load previous msg via ws
    user_id = 2


    chat_id = await service.save_chat(db, user_id, chat_id)
    await websocket.accept()
    while True:
        data = MlQuery.model_validate(await websocket.receive_json())

        async for msg in service.inference(db, ml_client, chat_id, data):
            await websocket.send_json(msg.model_dump())
