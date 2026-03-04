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
    x_signature_ed25519: str = Header(None),
    x_signature_timestamp: str = Header(None),
) -> bytes:
    """Verify the Discord Ed25519 request signature.

    In local mode (MODE=local), signature verification is skipped.
    Returns the raw request body for potential forwarding.
    """
    body = await request.body()

    # Skip verification in local mode
    if settings.MODE == "local":
        logger.warning(
            "MODE=local: Skipping signature verification. "
            "Ensure this is not running in production."
        )
        return body

    # Require headers in non-local modes
    if not x_signature_ed25519 or not x_signature_timestamp:
        logger.error("Missing signature headers in non-local mode")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing signature headers",
        )

    signature = x_signature_ed25519
    timestamp = x_signature_timestamp
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

    return body
