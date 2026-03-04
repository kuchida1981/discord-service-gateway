"""Tests for the main application health check endpoint."""

from unittest.mock import patch

from fastapi.testclient import TestClient

from src.main import app


def test_health_check() -> None:
    """Test that the health check endpoint returns 200 with status ok."""
    with patch("src.main.register_commands"), TestClient(app) as client:
        response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_health_check_with_registration_failure() -> None:
    """Test that the server starts even if register_commands raises."""
    error = RuntimeError("test error")
    patcher = patch("src.main.register_commands", side_effect=error)
    with patcher, TestClient(app) as client:
        response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
