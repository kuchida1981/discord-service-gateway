"""FastAPI dependencies for the Discord interaction API."""

import logging

from fastapi import Header, HTTPException, Request, status
from nacl.exceptions import BadSignatureError
from nacl.signing import VerifyKey

from src.core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def verify_discord_signature(
    request: Request,
    x_signature_ed25519: str = Header(...),
    x_signature_timestamp: str = Header(...),
) -> None:
    """Verify the Discord Ed25519 request signature."""
    signature = x_signature_ed25519
    timestamp = x_signature_timestamp
    body = await request.body()

    message = timestamp.encode() + body

    try:
        logger.info(
            "Verifying signature with Public Key starting with: %s...",
            settings.DISCORD_PUBLIC_KEY[:4],
        )
        verify_key = VerifyKey(bytes.fromhex(settings.DISCORD_PUBLIC_KEY))
        verify_key.verify(message, bytes.fromhex(signature))
        logger.info("Signature verification successful.")
    except (BadSignatureError, ValueError) as e:
        logger.error("Signature verification failed: %s", e)  # noqa: TRY400
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid request signature",
        ) from None
