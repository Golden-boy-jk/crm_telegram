from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Settings(Base):
    __tablename__ = "settings"

    id: Mapped[int] = mapped_column(primary_key=True)
    default_timezone: Mapped[str] = mapped_column(String(64), default="Europe/Moscow")
    allow_media: Mapped[bool] = mapped_column(Boolean, default=True)
