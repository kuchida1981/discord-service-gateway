"""Tests for the Discord interactions endpoint."""

import json

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
