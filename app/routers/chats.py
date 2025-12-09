from fastapi import APIRouter

router = APIRouter(prefix="/chats", tags=["chats"])


@router.get("")
async def list_chats() -> dict:
    return {"items": []}
