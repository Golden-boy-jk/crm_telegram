from collections import defaultdict
from typing import Dict, Set

from fastapi import WebSocket


class WebSocketManager:
    def __init__(self) -> None:
        self._connections: Dict[int, Set[WebSocket]] = defaultdict(set)

    async def connect(self, chat_id: int, websocket: WebSocket) -> None:
        await websocket.accept()
        self._connections[chat_id].add(websocket)

    def disconnect(self, chat_id: int, websocket: WebSocket) -> None:
        if chat_id in self._connections:
            self._connections[chat_id].discard(websocket)
            if not self._connections[chat_id]:
                del self._connections[chat_id]

    async def send_to_chat(self, chat_id: int, message: dict) -> None:
        for ws in list(self._connections.get(chat_id, [])):
            try:
                await ws.send_json(message)
            except Exception:
                self.disconnect(chat_id, ws)
