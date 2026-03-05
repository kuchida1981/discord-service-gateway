"""n8n service integration."""

import logging

import httpx

from src.core.config import settings

logger = logging.getLogger(__name__)


async def check_health() -> tuple[bool, str]:
    """Check n8n health status.

    Returns:
        Tuple of (is_healthy, message) where message describes the result.

    """
    try:
        async with httpx.AsyncClient(timeout=2.5) as client:
            response = await client.get(settings.N8N_HEALTH_URL)
            response.raise_for_status()
            data = response.json()
            status = data.get("status", "")
            if status == "ok":
                return True, "n8n status: ok ✅"
            return False, f"n8n status: error ❌ (unexpected status: {status})"
    except httpx.TimeoutException:
        logger.warning("Timeout connecting to n8n health endpoint")
        return False, "n8n status: error ❌ (timeout)"
    except httpx.HTTPStatusError as e:
        logger.warning("n8n health check returned HTTP %s", e.response.status_code)
        return False, f"n8n status: error ❌ (HTTP {e.response.status_code})"
    except Exception as e:
        logger.exception("Unexpected error during n8n health check")
        return False, f"n8n status: error ❌ ({e})"
