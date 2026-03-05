"""Tests for the Discord interactions endpoint."""

import json
from unittest.mock import AsyncMock, MagicMock

import httpx
import pytest
from fastapi.testclient import TestClient
from nacl.signing import SigningKey

from src.core.config import settings
from src.main import app

client = TestClient(app)


def test_interactions_ping_pong_success(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test that a PING interaction returns a PONG response."""
    signing_key = SigningKey.generate()
    public_key = signing_key.verify_key.encode().hex()

    monkeypatch.setattr(settings, "DISCORD_PUBLIC_KEY", public_key)

    payload = {"type": 1}
    body = json.dumps(payload).encode()
    timestamp = "1234567890"

    message = timestamp.encode() + body
    signature = signing_key.sign(message).signature.hex()

    response = client.post(
        "/interactions",
        content=body,
        headers={
            "X-Signature-Ed25519": signature,
            "X-Signature-Timestamp": timestamp,
        },
    )

    assert response.status_code == 200
    assert response.json() == {"type": 1}


def test_interactions_slash_command_ping_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test that the /ping slash command returns a Pong! message."""
    signing_key = SigningKey.generate()
    public_key = signing_key.verify_key.encode().hex()

    monkeypatch.setattr(settings, "DISCORD_PUBLIC_KEY", public_key)

    payload = {
        "type": 2,
        "data": {
            "name": "ping",
            "type": 1,
        },
    }
    body = json.dumps(payload).encode()
    timestamp = "1234567890"

    message = timestamp.encode() + body
    signature = signing_key.sign(message).signature.hex()

    response = client.post(
        "/interactions",
        content=body,
        headers={
            "X-Signature-Ed25519": signature,
            "X-Signature-Timestamp": timestamp,
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "type": 4,
        "data": {"content": "Pong!"},
    }


def test_interactions_unknown_type_returns_received(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test that an unknown interaction type returns a generic received response."""
    signing_key = SigningKey.generate()
    public_key = signing_key.verify_key.encode().hex()

    monkeypatch.setattr(settings, "DISCORD_PUBLIC_KEY", public_key)

    payload = {"type": 99}
    body = json.dumps(payload).encode()
    timestamp = "1234567890"

    message = timestamp.encode() + body
    signature = signing_key.sign(message).signature.hex()

    response = client.post(
        "/interactions",
        content=body,
        headers={
            "X-Signature-Ed25519": signature,
            "X-Signature-Timestamp": timestamp,
        },
    )

    assert response.status_code == 200
    assert response.json() == {"message": "received"}


def test_interactions_invalid_signature() -> None:
    """Test that an invalid signature returns 401 Unauthorized."""
    response = client.post(
        "/interactions",
        json={"type": 1},
        headers={
            "X-Signature-Ed25519": "invalid_signature",
            "X-Signature-Timestamp": "1234567890",
        },
    )

    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid request signature"}


def test_interactions_missing_signature_headers() -> None:
    """Test that missing signature headers return 401 in non-local mode."""
    response = client.post(
        "/interactions",
        json={"type": 1},
    )

    assert response.status_code == 401
    assert response.json() == {"detail": "Missing signature headers"}


def test_interactions_local_mode_skips_verification(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test that MODE=local skips signature verification."""
    monkeypatch.setattr(settings, "MODE", "local")

    payload = {"type": 1}
    response = client.post("/interactions", json=payload)

    assert response.status_code == 200
    assert response.json() == {"type": 1}


def _signed_request(
    monkeypatch: pytest.MonkeyPatch, payload: dict[str, object]
) -> tuple[bytes, dict[str, str]]:
    """Create a signed request payload and headers."""
    signing_key = SigningKey.generate()
    public_key = signing_key.verify_key.encode().hex()
    monkeypatch.setattr(settings, "DISCORD_PUBLIC_KEY", public_key)

    body = json.dumps(payload).encode()
    timestamp = "1234567890"
    message = timestamp.encode() + body
    signature = signing_key.sign(message).signature.hex()

    headers = {
        "X-Signature-Ed25519": signature,
        "X-Signature-Timestamp": timestamp,
    }
    return body, headers


def test_interactions_dev_mode_forwards_request_with_proxy_secret(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test that MODE=dev forwards request with PROXY_SECRET header when set."""
    monkeypatch.setattr(settings, "MODE", "dev")
    monkeypatch.setattr(settings, "FORWARD_URL", "https://example.ngrok.app")
    monkeypatch.setattr(settings, "PROXY_SECRET", "secret123")

    body, headers = _signed_request(monkeypatch, {"type": 1})

    mock_response = MagicMock()
    mock_response.json.return_value = {"type": 1}
    mock_response.status_code = 200

    mock_client = AsyncMock()
    mock_client.post = AsyncMock(return_value=mock_response)
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=None)

    monkeypatch.setattr("src.api.routes.httpx.AsyncClient", lambda **_: mock_client)

    response = client.post("/interactions", content=body, headers=headers)

    assert response.status_code == 200
    assert response.json() == {"type": 1}


def test_interactions_dev_mode_warns_on_http_with_proxy_secret(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test that a warning is logged when PROXY_SECRET is used over HTTP."""
    monkeypatch.setattr(settings, "MODE", "dev")
    monkeypatch.setattr(settings, "FORWARD_URL", "http://localhost:8000")
    monkeypatch.setattr(settings, "PROXY_SECRET", "secret123")

    body, headers = _signed_request(monkeypatch, {"type": 1})

    mock_response = MagicMock()
    mock_response.json.return_value = {"type": 1}
    mock_response.status_code = 200

    mock_client = AsyncMock()
    mock_client.post = AsyncMock(return_value=mock_response)
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=None)

    monkeypatch.setattr("src.api.routes.httpx.AsyncClient", lambda **_: mock_client)

    response = client.post("/interactions", content=body, headers=headers)

    assert response.status_code == 200


def test_interactions_dev_mode_forwards_request(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test that MODE=dev forwards request to FORWARD_URL."""
    monkeypatch.setattr(settings, "MODE", "dev")
    monkeypatch.setattr(settings, "FORWARD_URL", "https://example.ngrok.app")

    body, headers = _signed_request(monkeypatch, {"type": 1})

    mock_response = MagicMock()
    mock_response.json.return_value = {"type": 1}
    mock_response.status_code = 200

    mock_client = AsyncMock()
    mock_client.post = AsyncMock(return_value=mock_response)
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=None)

    monkeypatch.setattr("src.api.routes.httpx.AsyncClient", lambda **_: mock_client)

    response = client.post("/interactions", content=body, headers=headers)

    assert response.status_code == 200
    assert response.json() == {"type": 1}


def test_interactions_dev_mode_no_forward_url(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test that MODE=dev without FORWARD_URL returns an error."""
    monkeypatch.setattr(settings, "MODE", "dev")
    monkeypatch.setattr(settings, "FORWARD_URL", None)

    body, headers = _signed_request(monkeypatch, {"type": 1})
    response = client.post("/interactions", content=body, headers=headers)

    assert response.status_code == 200
    assert response.json() == {"error": "FORWARD_URL not configured"}


def test_interactions_dev_mode_timeout(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test that a timeout during forwarding returns an error."""
    monkeypatch.setattr(settings, "MODE", "dev")
    monkeypatch.setattr(settings, "FORWARD_URL", "https://example.ngrok.app")

    body, headers = _signed_request(monkeypatch, {"type": 1})

    mock_client = AsyncMock()
    mock_client.post = AsyncMock(side_effect=httpx.TimeoutException("timeout"))
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=None)

    monkeypatch.setattr("src.api.routes.httpx.AsyncClient", lambda **_: mock_client)

    response = client.post("/interactions", content=body, headers=headers)

    assert response.status_code == 200
    assert response.json() == {"error": "Forwarding timeout"}


def test_interactions_dev_mode_forwarding_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test that a generic error during forwarding returns an error."""
    monkeypatch.setattr(settings, "MODE", "dev")
    monkeypatch.setattr(settings, "FORWARD_URL", "https://example.ngrok.app")

    body, headers = _signed_request(monkeypatch, {"type": 1})

    mock_client = AsyncMock()
    mock_client.post = AsyncMock(side_effect=Exception("connection error"))
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=None)

    monkeypatch.setattr("src.api.routes.httpx.AsyncClient", lambda **_: mock_client)

    response = client.post("/interactions", content=body, headers=headers)

    assert response.status_code == 200
    assert response.json() == {"error": "Forwarding failed"}


def test_interactions_dsg_n8n_health_success(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test that /dsg n8n health returns ok message when n8n is healthy."""
    body, headers = _signed_request(
        monkeypatch,
        {
            "type": 2,
            "data": {
                "name": "dsg",
                "type": 1,
                "options": [
                    {
                        "name": "n8n",
                        "type": 2,
                        "options": [{"name": "health", "type": 1}],
                    }
                ],
            },
        },
    )

    mock_response = MagicMock()
    mock_response.json.return_value = {"status": "ok"}
    mock_response.raise_for_status = MagicMock()

    mock_client = AsyncMock()
    mock_client.get = AsyncMock(return_value=mock_response)
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=None)

    monkeypatch.setattr("src.services.n8n.httpx.AsyncClient", lambda **_: mock_client)

    response = client.post("/interactions", content=body, headers=headers)

    assert response.status_code == 200
    assert response.json() == {
        "type": 4,
        "data": {"content": "n8n status: ok ✅"},
    }


def test_interactions_dsg_n8n_health_failure(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test that /dsg n8n health returns error message when n8n is unhealthy."""
    body, headers = _signed_request(
        monkeypatch,
        {
            "type": 2,
            "data": {
                "name": "dsg",
                "type": 1,
                "options": [
                    {
                        "name": "n8n",
                        "type": 2,
                        "options": [{"name": "health", "type": 1}],
                    }
                ],
            },
        },
    )

    mock_client = AsyncMock()
    mock_client.get = AsyncMock(side_effect=httpx.TimeoutException("timeout"))
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=None)

    monkeypatch.setattr("src.services.n8n.httpx.AsyncClient", lambda **_: mock_client)

    response = client.post("/interactions", content=body, headers=headers)

    assert response.status_code == 200
    assert response.json() == {
        "type": 4,
        "data": {"content": "n8n status: error ❌ (timeout)"},
    }
