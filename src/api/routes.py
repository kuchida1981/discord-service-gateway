"""Discord interaction API routes."""

import json
import logging

import httpx
from fastapi import APIRouter, BackgroundTasks, Depends, Header, Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from src.api import handlers, models
from src.api.deps import verify_discord_signature
from src.core.config import settings
from src.core.constants import InteractionResponseType, InteractionType

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/")
async def health_check() -> dict[str, str]:
    """Return health check status."""
    return {"status": "ok"}


async def _forward_to_dev(
    request: Request,
    verified_body: bytes,
    x_signature_ed25519: str | None,
    x_signature_timestamp: str | None,
) -> dict[str, object] | JSONResponse:
    """Forward request to local dev environment."""
    if not settings.FORWARD_URL:
        logger.error("MODE=dev but FORWARD_URL is not set")
        return {"error": "FORWARD_URL not configured"}

    logger.info("MODE=dev: Forwarding request to %s", settings.FORWARD_URL)

    forward_headers: dict[str, str] = {
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


@router.post("/interactions", response_model=None)
async def interactions(
    request: Request,
    background_tasks: BackgroundTasks,
    verified_body: bytes = Depends(verify_discord_signature),
    x_signature_ed25519: str = Header(None),
    x_signature_timestamp: str = Header(None),
) -> dict[str, object] | JSONResponse:
    """Handle Discord interactions.

    In dev mode (MODE=dev), forwards requests to FORWARD_URL.
    In prod/local modes, processes interactions normally.
    """
    if settings.MODE == "dev":
        return await _forward_to_dev(
            request, verified_body, x_signature_ed25519, x_signature_timestamp
        )

    try:
        interaction_data = json.loads(verified_body)
        interaction = models.Interaction.model_validate(interaction_data)
    except (json.JSONDecodeError, ValidationError):
        logger.exception("Invalid interaction data")
        return JSONResponse(content={"error": "Invalid interaction"}, status_code=400)

    if interaction.type == InteractionType.PING:
        return {"type": InteractionResponseType.PONG}

    if interaction.type == InteractionType.APPLICATION_COMMAND:
        if interaction.data is None:
            return JSONResponse(
                content={"error": "Missing data for application command"},
                status_code=400,
            )
        result = await handlers.handle_application_command(
            interaction.data,
            background_tasks=background_tasks,
            token=interaction.token,
            application_id=interaction.application_id,
        )
        if result is not None:
            return result

    return {"message": "received"}
