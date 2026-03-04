"""Discord interaction API routes."""

from fastapi import APIRouter, Depends, Request

from src.api.deps import verify_discord_signature
from src.core.constants import InteractionResponseType, InteractionType

router = APIRouter()


@router.get("/")
async def health_check() -> dict[str, str]:
    """Return health check status."""
    return {"status": "ok"}


@router.post("/interactions", dependencies=[Depends(verify_discord_signature)])
async def interactions(request: Request) -> dict[str, object]:
    """Handle Discord interactions."""
    interaction = await request.json()

    if interaction.get("type") == InteractionType.PING:
        return {"type": InteractionResponseType.PONG}

    if interaction.get("type") == InteractionType.APPLICATION_COMMAND:
        data = interaction.get("data", {})
        if data.get("name") == "ping":
            return {
                "type": InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
                "data": {"content": "Pong!"},
            }

    return {"message": "received"}