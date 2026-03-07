"""Tests for the n8n service integration."""

from unittest.mock import AsyncMock, MagicMock

import httpx
import pytest

from src.services import n8n as n8n_service


@pytest.mark.asyncio
async def test_check_health_ok(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test that check_health returns True and ok message on healthy response."""
    mock_response = MagicMock()
    mock_response.json.return_value = {"status": "ok"}
    mock_response.raise_for_status = MagicMock()

    mock_client = AsyncMock()
    mock_client.get = AsyncMock(return_value=mock_response)
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=None)

    monkeypatch.setattr("src.services.n8n.httpx.AsyncClient", lambda **_: mock_client)

    is_healthy, message = await n8n_service.check_health()

    assert is_healthy is True
    assert message == "n8n status: ok ✅"


@pytest.mark.asyncio
async def test_check_health_unexpected_status(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test that check_health returns False when status is not 'ok'."""
    mock_response = MagicMock()
    mock_response.json.return_value = {"status": "degraded"}
    mock_response.raise_for_status = MagicMock()

    mock_client = AsyncMock()
    mock_client.get = AsyncMock(return_value=mock_response)
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=None)

    monkeypatch.setattr("src.services.n8n.httpx.AsyncClient", lambda **_: mock_client)

    is_healthy, message = await n8n_service.check_health()

    assert is_healthy is False
    assert "degraded" in message
    assert "❌" in message


@pytest.mark.asyncio
async def test_check_health_timeout(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test that check_health returns False on timeout."""
    mock_client = AsyncMock()
    mock_client.get = AsyncMock(side_effect=httpx.TimeoutException("timeout"))
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=None)

    monkeypatch.setattr("src.services.n8n.httpx.AsyncClient", lambda **_: mock_client)

    is_healthy, message = await n8n_service.check_health()

    assert is_healthy is False
    assert "timeout" in message
    assert "❌" in message


@pytest.mark.asyncio
async def test_check_health_http_error(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test that check_health returns False on HTTP error status."""
    mock_response = MagicMock()
    mock_response.status_code = 503

    mock_client = AsyncMock()
    mock_client.get = AsyncMock(
        side_effect=httpx.HTTPStatusError(
            "Service Unavailable",
            request=MagicMock(),
            response=mock_response,
        )
    )
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=None)

    monkeypatch.setattr("src.services.n8n.httpx.AsyncClient", lambda **_: mock_client)

    is_healthy, message = await n8n_service.check_health()

    assert is_healthy is False
    assert "503" in message
    assert "❌" in message


@pytest.mark.asyncio
async def test_get_tasks_list_plain_text(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test that get_tasks_list returns text body when content-type is text/plain."""
    mock_response = MagicMock()
    mock_response.headers = {"content-type": "text/plain"}
    mock_response.text = "### 📝 Google Tasks\n- [ ] タスク1"
    mock_response.raise_for_status = MagicMock()

    mock_client = AsyncMock()
    mock_client.post = AsyncMock(return_value=mock_response)
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=None)

    monkeypatch.setattr("src.services.n8n.httpx.AsyncClient", lambda **_: mock_client)

    result = await n8n_service.get_tasks_list()

    assert result == "### 📝 Google Tasks\n- [ ] タスク1"


@pytest.mark.asyncio
async def test_get_tasks_list_json_content(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test that get_tasks_list returns content field when content-type is application/json."""
    mock_response = MagicMock()
    mock_response.headers = {"content-type": "application/json"}
    mock_response.json.return_value = {"content": "### 📝 タスク一覧\n- [ ] タスク1"}
    mock_response.raise_for_status = MagicMock()

    mock_client = AsyncMock()
    mock_client.post = AsyncMock(return_value=mock_response)
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=None)

    monkeypatch.setattr("src.services.n8n.httpx.AsyncClient", lambda **_: mock_client)

    result = await n8n_service.get_tasks_list()

    assert result == "### 📝 タスク一覧\n- [ ] タスク1"


@pytest.mark.asyncio
async def test_get_tasks_list_empty_response(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test that get_tasks_list returns empty-state message when response text is empty."""
    mock_response = MagicMock()
    mock_response.headers = {"content-type": "text/plain"}
    mock_response.text = ""
    mock_response.raise_for_status = MagicMock()

    mock_client = AsyncMock()
    mock_client.post = AsyncMock(return_value=mock_response)
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=None)

    monkeypatch.setattr("src.services.n8n.httpx.AsyncClient", lambda **_: mock_client)

    result = await n8n_service.get_tasks_list()

    assert result == "現在アクティブなタスクはありません。"


@pytest.mark.asyncio
async def test_get_tasks_list_http_error(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test that get_tasks_list raises on HTTP error."""
    mock_response = MagicMock()
    mock_response.status_code = 500

    mock_client = AsyncMock()
    mock_client.post = AsyncMock(
        side_effect=httpx.HTTPStatusError(
            "Internal Server Error",
            request=MagicMock(),
            response=mock_response,
        )
    )
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=None)

    monkeypatch.setattr("src.services.n8n.httpx.AsyncClient", lambda **_: mock_client)

    with pytest.raises(httpx.HTTPStatusError):
        await n8n_service.get_tasks_list()


@pytest.mark.asyncio
async def test_check_health_generic_exception(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test that check_health returns False on unexpected errors."""
    mock_client = AsyncMock()
    mock_client.get = AsyncMock(side_effect=Exception("connection refused"))
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=None)

    monkeypatch.setattr("src.services.n8n.httpx.AsyncClient", lambda **_: mock_client)

    is_healthy, message = await n8n_service.check_health()

    assert is_healthy is False
    assert "connection refused" in message
    assert "❌" in message
