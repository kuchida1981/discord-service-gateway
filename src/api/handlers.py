"""Discord interaction command handlers."""

import logging

import httpx
from fastapi import BackgroundTasks

from src.api import models
from src.core.constants import InteractionResponseType
from src.services import n8n as n8n_service

logger = logging.getLogger(__name__)

DISCORD_WEBHOOK_BASE = "https://discord.com/api/v10/webhooks"


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


async def update_tasks_list_background(token: str, application_id: str) -> None:
    """Fetch tasks from n8n and update the Discord deferred message."""
    url = f"{DISCORD_WEBHOOK_BASE}/{application_id}/{token}/messages/@original"
    try:
        content = await n8n_service.get_tasks_list()
    except Exception:
        logger.exception("Failed to fetch tasks list from n8n")
        content = "タスクの取得に失敗しました。"

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.patch(url, json={"content": content})
            response.raise_for_status()
    except Exception:
        logger.exception("Failed to update Discord message via webhook")


def handle_dsg_tasks_list(
    background_tasks: BackgroundTasks,
    token: str,
    application_id: str,
) -> dict[str, object]:
    """Handle the /dsg tasks list subcommand."""
    background_tasks.add_task(update_tasks_list_background, token, application_id)
    return {"type": InteractionResponseType.DEFERRED_CHANNEL_MESSAGE_WITH_SOURCE}


async def handle_dsg_command(
    data: models.DsgCommandData,
    background_tasks: BackgroundTasks | None = None,
    token: str | None = None,
    application_id: str | None = None,
) -> dict[str, object] | None:
    """Handle the /dsg command."""
    group = data.options[0]
    if group.name == "n8n":
        sub_option = group.options[0]
        if sub_option.name == "health":
            return await handle_dsg_n8n_health()

    if group.name == "tasks":
        sub_option = group.options[0]
        if sub_option.name == "list":
            if background_tasks is not None and token and application_id:
                return handle_dsg_tasks_list(background_tasks, token, application_id)

    return None


async def handle_application_command(
    data: models.CommandData,
    background_tasks: BackgroundTasks | None = None,
    token: str | None = None,
    application_id: str | None = None,
) -> dict[str, object] | None:
    """Dispatch an application command to its handler, or None if unhandled."""
    if isinstance(data, models.PingCommandData):
        return handle_ping()

    if isinstance(data, models.DsgCommandData):
        return await handle_dsg_command(
            data,
            background_tasks=background_tasks,
            token=token,
            application_id=application_id,
        )

    return None
