from typing import Optional

from sqlalchemy import BigInteger, Boolean, ForeignKey, JSON, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class WebhookEvent(Base):
    __tablename__ = "webhook_events"
    __table_args__ = (
        UniqueConstraint("bot_id", "update_id", name="uq_bot_update"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    bot_id: Mapped[int] = mapped_column(ForeignKey("bots.id"), index=True)
    update_id: Mapped[int] = mapped_column(BigInteger)
    processed: Mapped[bool] = mapped_column(Boolean, default=False)
    payload: Mapped[dict] = mapped_column(JSON)
    error: Mapped[Optional[str]] = mapped_column(String, nullable=True)
