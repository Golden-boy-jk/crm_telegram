from typing import Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.models.contact import Contact

router = APIRouter(prefix="/contacts", tags=["contacts"])


class ContactIn(BaseModel):
    telegram_user_id: int
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    photo_url: Optional[str] = None


class ContactOut(ContactIn):
    id: int


@router.post("", response_model=ContactOut)
async def upsert_contact(
    payload: ContactIn,
    session: AsyncSession = Depends(get_session),
) -> ContactOut:
    q = select(Contact).where(Contact.telegram_user_id == payload.telegram_user_id)
    contact = (await session.execute(q)).scalar_one_or_none()

    if contact is None:
        contact = Contact(**payload.model_dump())
        session.add(contact)
    else:
        for k, v in payload.model_dump().items():
            if v is not None:
                setattr(contact, k, v)

    await session.commit()
    await session.refresh(contact)

    return ContactOut(id=contact.id, **payload.model_dump())
