"""Script to register Discord slash commands."""

import argparse
import logging
import sys

import httpx

from src.core.config import settings
from src.core.exceptions import MissingApplicationIdError, MissingTokenError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def register_commands() -> None:
    """Register slash commands with the Discord API."""
    app_id = settings.DISCORD_APPLICATION_ID
    token = settings.DISCORD_TOKEN
    guild_id = settings.DISCORD_GUILD_ID

    if not token or token == "dummy_token":
        raise MissingTokenError()

    if not app_id or app_id == "dummy_app_id":
        raise MissingApplicationIdError()

    # Define commands
    commands = [
        {
            "name": "ping",
            "description": "Replies with Pong!",
            "type": 1,  # CHAT_INPUT
        },
        {
            "name": "dsg",
            "description": "Discord Service Gateway commands",
            "type": 1,  # CHAT_INPUT
            "options": [
                {
                    "name": "n8n",
                    "description": "n8n workflow automation commands",
                    "type": 2,  # SUB_COMMAND_GROUP
                    "options": [
                        {
                            "name": "health",
                            "description": "Check n8n health status",
                            "type": 1,  # SUB_COMMAND
                        }
                    ],
                }
            ],
        },
    ]
    logger.info(
        "Registering %d command(s): %s", len(commands), [c["name"] for c in commands]
    )

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
        logger.exception("HTTP error occurred. Response: %s", e.response.text)
        raise
    except Exception:
        logger.exception("An error occurred")
        raise


def main() -> None:
    """Run the CLI entrypoint."""
    parser = argparse.ArgumentParser(
        description="Register Discord slash commands via the Discord API"
    )
    parser.parse_args()

    try:
        register_commands()
    except Exception:
        logger.exception("Command registration failed")
        sys.exit(1)


if __name__ == "__main__":  # pragma: no cover
    main()
