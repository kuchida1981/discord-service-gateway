from fastapi import Header, HTTPException, Request, status
from nacl.exceptions import BadSignatureError
from nacl.signing import VerifyKey

from src.core.config import settings


async def verify_discord_signature(
    request: Request,
    x_signature_ed25519: str = Header(...),
    x_signature_timestamp: str = Header(...),
) -> None:
    signature = x_signature_ed25519
    timestamp = x_signature_timestamp
    body = await request.body()

    message = timestamp.encode() + body
    
    try:
        verify_key = VerifyKey(bytes.fromhex(settings.DISCORD_PUBLIC_KEY))
        verify_key.verify(message, bytes.fromhex(signature))
    except (BadSignatureError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid request signature",
        ) from None
