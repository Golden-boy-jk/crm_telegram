from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.models.chat import Chat
from app.models.contact import Contact
from app.models.message import Message

router = APIRouter(prefix="/chats", tags=["chats"])


class ContactOut(BaseModel):
    id: int
    telegram_user_id: int
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    photo_url: Optional[str] = None


class LastMsgOut(BaseModel):
    direction: Optional[str] = None
    content_text: Optional[str] = None
    timestamp: Optional[datetime] = None


class ChatOut(BaseModel):
    id: int
    bot_id: int
    contact: ContactOut
    last_message_at: Optional[datetime] = None
    unread_count: int
    last_message: LastMsgOut


@router.get("", response_model=dict)
async def list_chats(
    session: AsyncSession = Depends(get_session),
    limit: int = 50,
    offset: int = 0,
) -> dict:
    last_text = (
        select(Message.content_text)
        .where(Message.chat_id == Chat.id)
        .order_by(Message.timestamp.desc())
        .limit(1)
        .scalar_subquery()
    )
    last_ts = (
        select(Message.timestamp)
        .where(Message.chat_id == Chat.id)
        .order_by(Message.timestamp.desc())
        .limit(1)
        .scalar_subquery()
    )
    last_dir = (
        select(Message.direction)
        .where(Message.chat_id == Chat.id)
        .order_by(Message.timestamp.desc())
        .limit(1)
        .scalar_subquery()
    )

    q = (
        select(
            Chat,
            Contact,
            last_text.label("last_text"),
            last_ts.label("last_ts"),
            last_dir.label("last_dir"),
        )
        .join(Contact, Contact.id == Chat.contact_id)
        .order_by(Chat.last_message_at.desc().nullslast(), Chat.id.desc())
        .limit(limit)
        .offset(offset)
    )

    rows = (await session.execute(q)).all()

    items = [
        ChatOut(
            id=chat.id,
            bot_id=chat.bot_id,
            contact=ContactOut(
                id=contact.id,
                telegram_user_id=contact.telegram_user_id,
                username=contact.username,
                first_name=contact.first_name,
                last_name=contact.last_name,
                photo_url=contact.photo_url,
            ),
            last_message_at=chat.last_message_at,
            unread_count=chat.unread_count,
            last_message=LastMsgOut(
                direction=last_dir,
                content_text=last_text,
                timestamp=last_ts,
            ),
        ).model_dump()
        for chat, contact, last_text, last_ts, last_dir in rows
    ]

    return {"items": items, "limit": limit, "offset": offset}
