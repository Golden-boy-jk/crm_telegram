from fastapi import APIRouter

router = APIRouter(prefix="/bots", tags=["bots"])


@router.get("")
async def list_bots() -> dict:
    return {"items": []}
