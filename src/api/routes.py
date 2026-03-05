"""Discord interaction API routes."""

import json
import logging

import httpx
from fastapi import APIRouter, Depends, Header, Request
from fastapi.responses import JSONResponse

from src.api.deps import verify_discord_signature
from src.core.config import settings
from src.core.constants import InteractionResponseType, InteractionType
from src.services import n8n as n8n_service

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/")
async def health_check() -> dict[str, str]:
    """Return health check status."""
    return {"status": "ok"}


@router.post("/interactions", response_model=None)
async def interactions(  # noqa: PLR0911, PLR0912
    request: Request,
    verified_body: bytes = Depends(verify_discord_signature),
    x_signature_ed25519: str = Header(None),
    x_signature_timestamp: str = Header(None),
) -> dict[str, object] | JSONResponse:
    """Handle Discord interactions.

    In dev mode (MODE=dev), forwards requests to FORWARD_URL.
    In prod/local modes, processes interactions normally.
    """
    # Forward to local environment in dev mode
    if settings.MODE == "dev":
        if not settings.FORWARD_URL:
            logger.error("MODE=dev but FORWARD_URL is not set")
            return {"error": "FORWARD_URL not configured"}

        logger.info("MODE=dev: Forwarding request to %s", settings.FORWARD_URL)

        # Prepare headers for forwarding
        forward_headers = {
            "Content-Type": request.headers.get("content-type", "application/json"),
        }
        if x_signature_ed25519:
            forward_headers["X-Signature-Ed25519"] = x_signature_ed25519
        if x_signature_timestamp:
            forward_headers["X-Signature-Timestamp"] = x_signature_timestamp
        if settings.PROXY_SECRET:
            if not settings.FORWARD_URL.startswith("https://"):
                logger.warning(
                    "PROXY_SECRET is set but FORWARD_URL is not HTTPS: %s",
                    settings.FORWARD_URL,
                )
            forward_headers["X-Proxy-Secret"] = settings.PROXY_SECRET

        try:
            async with httpx.AsyncClient(timeout=3.0) as client:
                response = await client.post(
                    f"{settings.FORWARD_URL}/interactions",
                    content=verified_body,
                    headers=forward_headers,
                )
                return JSONResponse(
                    content=response.json(),
                    status_code=response.status_code,
                )
        except httpx.TimeoutException:
            logger.exception("Timeout forwarding to %s", settings.FORWARD_URL)
            return {"error": "Forwarding timeout"}
        except Exception:
            logger.exception("Error forwarding request")
            return {"error": "Forwarding failed"}

    # Normal processing in prod/local mode
    interaction = json.loads(verified_body)

    if interaction.get("type") == InteractionType.PING:
        return {"type": InteractionResponseType.PONG}

    if interaction.get("type") == InteractionType.APPLICATION_COMMAND:
        data = interaction.get("data", {})
        if data.get("name") == "ping":
            return {
                "type": InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
                "data": {"content": "Pong!"},
            }
        if data.get("name") == "dsg":
            options = data.get("options", [])
            if options:
                group = options[0]
                if group.get("name") == "n8n":
                    sub_options = group.get("options", [])
                    if sub_options and sub_options[0].get("name") == "health":
                        _, message = await n8n_service.check_health()
                        return {
                            "type": InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
                            "data": {"content": message},
                        }

    return {"message": "received"}
