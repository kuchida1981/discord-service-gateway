"""Script to register Discord slash commands."""

import logging
import sys

import httpx

from src.core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def register_commands() -> None:
    """Register slash commands with the Discord API."""
    app_id = settings.DISCORD_APPLICATION_ID
    token = settings.DISCORD_TOKEN
    guild_id = settings.DISCORD_GUILD_ID

    if not token or token == "dummy_token":  # noqa: S105
        logger.error("Error: DISCORD_TOKEN is not set.")
        sys.exit(1)

    if not app_id or app_id == "dummy_app_id":
        logger.error("Error: DISCORD_APPLICATION_ID is not set.")
        sys.exit(1)

    # Define commands
    commands = [
        {
            "name": "ping",
            "description": "Replies with Pong!",
            "type": 1,  # CHAT_INPUT
        }
    ]

    # Registration URL
    if guild_id:
        url = f"https://discord.com/api/v10/applications/{app_id}/guilds/{guild_id}/commands"
        logger.info("Registering commands to guild: %s", guild_id)
    else:
        url = f"https://discord.com/api/v10/applications/{app_id}/commands"
        logger.info("Registering global commands")

    headers = {
        "Authorization": f"Bot {token}",
        "Content-Type": "application/json",
    }

    try:
        response = httpx.put(url, headers=headers, json=commands)
        response.raise_for_status()
        logger.info("Successfully registered commands: %s", response.status_code)
        logger.info("%s", response.json())
    except httpx.HTTPStatusError as e:
        logger.exception("HTTP error occurred")
        logger.error("Response: %s", e.response.text)  # noqa: TRY400
        sys.exit(1)
    except Exception:
        logger.exception("An error occurred")
        sys.exit(1)


if __name__ == "__main__":
    register_commands()