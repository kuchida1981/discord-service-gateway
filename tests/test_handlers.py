"""Unit tests for command handlers."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi import BackgroundTasks

from src.api import handlers, models
from src.core.constants import InteractionResponseType


@pytest.mark.asyncio
async def test_handle_application_command_ping() -> None:
    """Test handle_application_command with /ping."""
    data = models.PingCommandData(name="ping", id="123", type=1)
    result = await handlers.handle_application_command(data)
    assert result is not None
    data_field = result.get("data")
    assert isinstance(data_field, dict)
    assert data_field.get("content") == "Pong!"


@pytest.mark.asyncio
async def test_handle_application_command_dsg_health(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test handle_application_command with /dsg n8n health."""
    data = models.DsgCommandData(
        name="dsg",
        id="123",
        type=1,
        options=[
            models.N8nGroup(
                name="n8n",
                type=2,
                options=[models.HealthOption(name="health", type=1)],
            )
        ],
    )

    mock_response = MagicMock()
    mock_response.json.return_value = {"status": "ok"}
    mock_response.raise_for_status = MagicMock()

    mock_client = AsyncMock()
    mock_client.get = AsyncMock(return_value=mock_response)
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=None)

    monkeypatch.setattr("src.services.n8n.httpx.AsyncClient", lambda **_: mock_client)

    result = await handlers.handle_application_command(data)
    assert result is not None
    data_field = result.get("data")
    assert isinstance(data_field, dict)
    assert "ok" in str(data_field.get("content"))


@pytest.mark.asyncio
async def test_handle_dsg_command_unknown_sub_option() -> None:
    """Test handle_dsg_command with unknown sub-option in n8n group."""

    class MockSubOption:
        name = "unknown"

    # Using model_construct to bypass validation for testing purposes
    group = models.N8nGroup.model_construct(
        name="n8n",
        type=2,
        options=[MockSubOption()],
    )
    data = models.DsgCommandData.model_construct(
        name="dsg",
        id="123",
        type=1,
        options=[group],
    )
    result = await handlers.handle_dsg_command(data)
    assert result is None


@pytest.mark.asyncio
async def test_handle_application_command_none() -> None:
    """Test handle_application_command with unknown command data type."""

    class MockCommandData:
        pass

    result = await handlers.handle_application_command(MockCommandData())  # type: ignore
    assert result is None


@pytest.mark.asyncio
async def test_handle_dsg_tasks_list_returns_deferred() -> None:
    """Test handle_dsg_tasks_list returns Type 5 deferred response."""
    background_tasks = BackgroundTasks()
    result = handlers.handle_dsg_tasks_list(
        background_tasks=background_tasks,
        token="test_token",
        application_id="test_app_id",
    )
    assert result["type"] == InteractionResponseType.DEFERRED_CHANNEL_MESSAGE_WITH_SOURCE


@pytest.mark.asyncio
async def test_handle_application_command_dsg_tasks_list(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test handle_application_command with /dsg tasks list."""
    data = models.DsgCommandData(
        name="dsg",
        id="123",
        type=1,
        options=[
            models.TasksGroup(
                name="tasks",
                type=2,
                options=[models.ListOption(name="list", type=1)],
            )
        ],
    )

    background_tasks = BackgroundTasks()
    result = await handlers.handle_application_command(
        data,
        background_tasks=background_tasks,
        token="test_token",
        application_id="test_app_id",
    )
    assert result is not None
    assert result["type"] == InteractionResponseType.DEFERRED_CHANNEL_MESSAGE_WITH_SOURCE


@pytest.mark.asyncio
async def test_update_tasks_list_background_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test update_tasks_list_background patches Discord message on success."""
    monkeypatch.setattr(
        "src.api.handlers.n8n_service.get_tasks_list",
        AsyncMock(return_value="### 📝 タスク一覧\n- [ ] タスク1"),
    )

    mock_response = MagicMock()
    mock_response.raise_for_status = MagicMock()

    mock_client = AsyncMock()
    mock_client.patch = AsyncMock(return_value=mock_response)
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=None)

    with patch("src.api.handlers.httpx.AsyncClient", return_value=mock_client):
        await handlers.update_tasks_list_background(
            token="test_token", application_id="test_app_id"
        )

    mock_client.patch.assert_called_once()
    call_kwargs = mock_client.patch.call_args
    assert "messages/@original" in call_kwargs[0][0]
    assert call_kwargs[1]["json"]["content"] == "### 📝 タスク一覧\n- [ ] タスク1"


@pytest.mark.asyncio
async def test_update_tasks_list_background_n8n_failure(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test update_tasks_list_background sends error message when n8n fails."""
    monkeypatch.setattr(
        "src.api.handlers.n8n_service.get_tasks_list",
        AsyncMock(side_effect=Exception("n8n unavailable")),
    )

    mock_response = MagicMock()
    mock_response.raise_for_status = MagicMock()

    mock_client = AsyncMock()
    mock_client.patch = AsyncMock(return_value=mock_response)
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=None)

    with patch("src.api.handlers.httpx.AsyncClient", return_value=mock_client):
        await handlers.update_tasks_list_background(
            token="test_token", application_id="test_app_id"
        )

    call_kwargs = mock_client.patch.call_args
    assert "失敗" in call_kwargs[1]["json"]["content"]


@pytest.mark.asyncio
async def test_update_tasks_list_background_discord_patch_failure(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test update_tasks_list_background handles Discord PATCH failure gracefully."""
    monkeypatch.setattr(
        "src.api.handlers.n8n_service.get_tasks_list",
        AsyncMock(return_value="### 📝 タスク一覧"),
    )

    mock_client = AsyncMock()
    mock_client.patch = AsyncMock(side_effect=Exception("Discord unreachable"))
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=None)

    with patch("src.api.handlers.httpx.AsyncClient", return_value=mock_client):
        # Should not raise even when Discord PATCH fails
        await handlers.update_tasks_list_background(
            token="test_token", application_id="test_app_id"
        )
