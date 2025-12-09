from fastapi import APIRouter

router = APIRouter(prefix="/telegram", tags=["telegram"])


@router.post("/webhook/{bot_id}")
async def telegram_webhook(bot_id: int, payload: dict) -> dict:
    # Здесь позже добавим обработку апдейтов Telegram и идемпотентность.
    return {"ok": True, "bot_id": bot_id}
