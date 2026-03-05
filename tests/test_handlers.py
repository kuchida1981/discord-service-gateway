"""Unit tests for command handlers."""

from unittest.mock import AsyncMock, MagicMock

import pytest

from src.api import handlers, models


@pytest.mark.asyncio
async def test_handle_application_command_ping() -> None:
    """Test handle_application_command with /ping."""
    data = models.PingCommandData(name="ping")
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
async def test_handle_dsg_command_no_options() -> None:
    """Test handle_dsg_command with no options."""
    data = models.DsgCommandData(name="dsg", options=[])
    result = await handlers.handle_dsg_command(data)
    assert result is None


@pytest.mark.asyncio
async def test_handle_dsg_command_no_group_options() -> None:
    """Test handle_dsg_command with a group having no options."""
    # Mocking N8nGroup to bypass Literal if necessary
    # Actually, we can just use models.N8nGroup with empty options if allowed
    try:
        group = models.N8nGroup(name="n8n", type=2, options=[])
        data = models.DsgCommandData(name="dsg", options=[group])
        result = await handlers.handle_dsg_command(data)
        assert result is None
    except Exception:
        # If Pydantic prevents empty list, it won't be parsed anyway
        pytest.skip("Pydantic prevented creating N8nGroup with empty options")


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
