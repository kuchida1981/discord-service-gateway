"""Discord interaction command handlers."""

from src.api import models
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


async def handle_dsg_command(data: models.DsgCommandData) -> dict[str, object] | None:
    """Handle the /dsg command."""
    # Since we only have /dsg n8n health for now, we can check the first option
    if not data.options:
        return None

    group = data.options[0]
    if group.name == "n8n":
        if not group.options:
            return None
        sub_option = group.options[0]
        if sub_option.name == "health":
            return await handle_dsg_n8n_health()

    return None


async def handle_application_command(
    data: models.CommandData,
) -> dict[str, object] | None:
    """Dispatch an application command to its handler, or None if unhandled."""
    if isinstance(data, models.PingCommandData):
        return handle_ping()

    if isinstance(data, models.DsgCommandData):
        return await handle_dsg_command(data)

    return None
