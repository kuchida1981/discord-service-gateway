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

    # Type 2: APPLICATION_COMMAND
    if interaction.get("type") == 2:
        data = interaction.get("data", {})
        if data.get("name") == "ping":
            return {
                "type": 4,  # CHANNEL_MESSAGE_WITH_SOURCE
                "data": {"content": "Pong!"},
            }

    return {"message": "received"}
