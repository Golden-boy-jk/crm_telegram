from fastapi import APIRouter

router = APIRouter(prefix="/contacts", tags=["contacts"])


@router.get("")
async def list_contacts() -> dict:
    return {"items": []}
