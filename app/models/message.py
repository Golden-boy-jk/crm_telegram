from datetime import datetime
from typing import Optional

from sqlalchemy import BigInteger, Boolean, DateTime, JSON, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class MessageDirection(str):
    INCOMING = "incoming"
    OUTGOING = "outgoing"


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(primary_key=True)
    chat_id: Mapped[int] = mapped_column(ForeignKey("chats.id"), index=True)

    direction: Mapped[str] = mapped_column(String(20))
    content_text: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    content_image_path: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)

    telegram_message_id: Mapped[Optional[int]] = mapped_column(
        BigInteger, index=True, nullable=True
    )

    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    is_read: Mapped[bool] = mapped_column(Boolean, default=False)

    meta: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)

    chat: Mapped["Chat"] = relationship(back_populates="messages")
