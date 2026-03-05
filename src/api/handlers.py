"""Discord interaction command handlers."""

from src.core.constants import InteractionResponseType
from src.services import n8n as n8n_service


def handle_ping() -> dict[str, object]:
    """Handle the /ping command."""
    return {
        "type": InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
        "data": {"content": "Pong!"},
    }


async def handle_dsg_n8n_health() -> dict[str, object]:
    """Handle the /dsg n8n health subcommand."""
    _, message = await n8n_service.check_health()
    return {
        "type": InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
        "data": {"content": message},
    }


async def handle_application_command(
    data: dict[str, object],
) -> dict[str, object] | None:
    """Dispatch an application command to its handler, or None if unhandled."""
    if data.get("name") == "ping":
        return handle_ping()
    if data.get("name") == "dsg":
        options = data.get("options", [])
        if isinstance(options, list) and options:
            group = options[0]
            if isinstance(group, dict) and group.get("name") == "n8n":
                sub_options = group.get("options", [])
                if isinstance(sub_options, list) and sub_options:
                    first = sub_options[0]
                    if isinstance(first, dict) and first.get("name") == "health":
                        return await handle_dsg_n8n_health()
    return None
