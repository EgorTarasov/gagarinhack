import uuid

from fastapi import APIRouter, WebSocket, Depends
from fastapi.responses import HTMLResponse
from data import get_connection
from asyncpg.pool import PoolConnectionProxy
import aiofiles
from . import service
from .schema import  MlQuery, MlResponse

router = APIRouter(prefix="/chat", tags=["chat"])


@router.get("/")
async def get():
    with open("./templates/chat.html") as file:
        html = file.read()
    return HTMLResponse(html)


@router.websocket("/ws/{chat_id}")
async def websocket_endpoint(
        websocket: WebSocket,
        chat_id: uuid.UUID,
        db: PoolConnectionProxy = Depends(get_connection),
):
    user_id = 2
    chat_id = await service.save_chat(db, user_id, chat_id)
    await websocket.accept()
    while True:
        data = MlQuery.model_validate(await websocket.receive_json())

        async for msg in service.inference(db, chat_id, data):
            await websocket.send_json(msg.model_dump())
