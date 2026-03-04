import logging
from fastapi import Header, HTTPException, Request, status
from nacl.exceptions import BadSignatureError
from nacl.signing import VerifyKey

from src.core.config import settings

# ログの設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
        # デバッグログ: 公開鍵の最初の数文字を表示して、読み込まれているか確認
        logger.info(f"Verifying signature with Public Key starting with: {settings.DISCORD_PUBLIC_KEY[:4]}...")
        
        verify_key = VerifyKey(bytes.fromhex(settings.DISCORD_PUBLIC_KEY))
        verify_key.verify(message, bytes.fromhex(signature))
        
        logger.info("Signature verification successful.")
    except (BadSignatureError, ValueError) as e:
        logger.error(f"Signature verification failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid request signature",
        ) from None
