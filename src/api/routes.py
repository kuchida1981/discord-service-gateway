from fastapi import APIRouter, Depends, Request

from src.api.deps import verify_discord_signature

router = APIRouter()


@router.get("/")
async def health_check():
    return {"status": "ok"}


@router.post("/interactions", dependencies=[Depends(verify_discord_signature)])
async def interactions(request: Request):
    interaction = await request.json()
    
    # Type 1: PING
    if interaction.get("type") == 1:
        return {"type": 1}

    return {"message": "received"}
