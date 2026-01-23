from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.models.webhook_event import WebhookEvent

router = APIRouter(prefix="/telegram", tags=["telegram"])


@router.post("/webhook/{bot_id}")
async def telegram_webhook(
    bot_id: int,
    payload: dict,
    session: AsyncSession = Depends(get_session),
) -> dict:
    update_id = payload.get("update_id")
    if update_id is None:
        raise HTTPException(status_code=400, detail="payload.update_id is required")

    ev = WebhookEvent(bot_id=bot_id, update_id=update_id, payload=payload, processed=False)
    session.add(ev)

    try:
        await session.commit()
        await session.refresh(ev)
        created = True
    except IntegrityError:
        await session.rollback()
        created = False
        ev = (
            await session.execute(
                select(WebhookEvent).where(
                    WebhookEvent.bot_id == bot_id,
                    WebhookEvent.update_id == update_id,
                )
            )
        ).scalar_one()

        if ev.processed:
            return {"ok": True, "duplicate": True, "processed": True}

    # TODO: здесь будет нормальная обработка апдейта (создание контакта/чата/сообщений)
    if not ev.processed:
        ev.processed = True
        await session.commit()

    return {"ok": True, "created": created, "processed": True}
