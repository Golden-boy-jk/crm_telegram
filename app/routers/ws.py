from fastapi import APIRouter, Depends, WebSocket

from app.ws.manager import WebSocketManager

router = APIRouter()
manager = WebSocketManager()


async def get_current_user() -> None:
    # заглушка для auth. Потом заменим реальной проверкой.
    return None


@router.websocket("/ws/chat/{chat_id}")
async def chat_ws(websocket: WebSocket, chat_id: int, _user=Depends(get_current_user)) -> None:
    await manager.connect(chat_id, websocket)
    try:
        while True:
            await websocket.receive_text()
    except Exception:
        pass
    finally:
        manager.disconnect(chat_id, websocket)
