"""Tests for CLI tools."""

import json
import subprocess
from unittest.mock import MagicMock, patch

import httpx
import pytest

from src.cli.register_commands import main as register_commands_main
from src.cli.register_commands import register_commands
from src.cli.toggle_mode import get_current_mode, main, run_command, toggle_mode

# --- register_commands tests ---


def test_register_commands_success() -> None:
    """Test successful command registration."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = [{"name": "ping"}]
    mock_response.raise_for_status = MagicMock()

    with (
        patch("src.cli.register_commands.settings") as mock_settings,
        patch("httpx.put", return_value=mock_response),
    ):
        mock_settings.DISCORD_APPLICATION_ID = "app123"
        mock_settings.DISCORD_TOKEN = "token123"  # noqa: S105
        mock_settings.DISCORD_GUILD_ID = "guild456"
        register_commands()

    mock_response.raise_for_status.assert_called_once()


def test_register_commands_global_when_no_guild() -> None:
    """Test global command registration when DISCORD_GUILD_ID is not set."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = []
    mock_response.raise_for_status = MagicMock()

    with (
        patch("src.cli.register_commands.settings") as mock_settings,
        patch("httpx.put", return_value=mock_response) as mock_put,
    ):
        mock_settings.DISCORD_APPLICATION_ID = "app123"
        mock_settings.DISCORD_TOKEN = "token123"  # noqa: S105
        mock_settings.DISCORD_GUILD_ID = None
        register_commands()

    called_url = mock_put.call_args[0][0]
    assert "/guilds/" not in called_url


def test_register_commands_raises_when_token_missing() -> None:
    """Test that missing DISCORD_TOKEN raises RuntimeError."""
    with patch("src.cli.register_commands.settings") as mock_settings:
        mock_settings.DISCORD_TOKEN = "dummy_token"  # noqa: S105
        mock_settings.DISCORD_APPLICATION_ID = "app123"
        mock_settings.DISCORD_GUILD_ID = None
        with pytest.raises(RuntimeError):
            register_commands()


def test_register_commands_raises_when_app_id_missing() -> None:
    """Test that missing DISCORD_APPLICATION_ID raises RuntimeError."""
    with patch("src.cli.register_commands.settings") as mock_settings:
        mock_settings.DISCORD_TOKEN = "real_token"  # noqa: S105
        mock_settings.DISCORD_APPLICATION_ID = "dummy_app_id"
        mock_settings.DISCORD_GUILD_ID = None
        with pytest.raises(RuntimeError):
            register_commands()


def test_register_commands_http_error() -> None:
    """Test that HTTP errors are re-raised."""
    mock_err_response = MagicMock()
    mock_err_response.text = "Forbidden"
    http_error = httpx.HTTPStatusError(
        "403", request=MagicMock(), response=mock_err_response
    )
    mock_put_response = MagicMock()
    mock_put_response.raise_for_status.side_effect = http_error

    with (
        patch("src.cli.register_commands.settings") as mock_settings,
        patch("httpx.put", return_value=mock_put_response),
    ):
        mock_settings.DISCORD_TOKEN = "real_token"  # noqa: S105
        mock_settings.DISCORD_APPLICATION_ID = "real_app"
        mock_settings.DISCORD_GUILD_ID = None
        with pytest.raises(httpx.HTTPStatusError):
            register_commands()


def test_register_commands_generic_error() -> None:
    """Test that generic errors are re-raised."""
    with (
        patch("src.cli.register_commands.settings") as mock_settings,
        patch("httpx.put", side_effect=ConnectionError("Network error")),
    ):
        mock_settings.DISCORD_TOKEN = "real_token"  # noqa: S105
        mock_settings.DISCORD_APPLICATION_ID = "real_app"
        mock_settings.DISCORD_GUILD_ID = None
        with pytest.raises(ConnectionError):
            register_commands()


# --- toggle_mode tests ---


def _make_proc(
    returncode: int = 0, stdout: str = "", stderr: str = ""
) -> subprocess.CompletedProcess[str]:
    return subprocess.CompletedProcess(
        args=[], returncode=returncode, stdout=stdout, stderr=stderr
    )


def test_run_command_success() -> None:
    """Test successful command execution."""
    with patch("subprocess.run", return_value=_make_proc(0, "ok")) as mock_run:
        result = run_command(["echo", "ok"])
    assert result.returncode == 0
    mock_run.assert_called_once()


def test_run_command_failure_exits() -> None:
    """Test that a failed command calls sys.exit."""
    with (
        patch("subprocess.run", return_value=_make_proc(1, stderr="oops")),
        pytest.raises(SystemExit),
    ):
        run_command(["false"])


def test_get_current_mode() -> None:
    """Test parsing of Cloud Run service description."""
    service_json = {
        "spec": {
            "template": {
                "spec": {"containers": [{"env": [{"name": "MODE", "value": "prod"}]}]}
            }
        }
    }
    mock_result = _make_proc(0, stdout=json.dumps(service_json))
    with patch("src.cli.toggle_mode.run_command", return_value=mock_result):
        env = get_current_mode("proj", "region", "svc")
    assert env["MODE"] == "prod"


def test_get_current_mode_empty_containers() -> None:
    """Test get_current_mode when spec has no containers."""
    service_json: dict[str, object] = {
        "spec": {"template": {"spec": {"containers": []}}}
    }
    mock_result = _make_proc(0, stdout=json.dumps(service_json))
    with patch("src.cli.toggle_mode.run_command", return_value=mock_result):
        env = get_current_mode("proj", "region", "svc")
    assert env == {}


def test_get_current_mode_no_spec() -> None:
    """Test get_current_mode when service data has no spec."""
    mock_result = _make_proc(0, stdout=json.dumps({}))
    with patch("src.cli.toggle_mode.run_command", return_value=mock_result):
        env = get_current_mode("proj", "region", "svc")
    assert env == {}


def test_toggle_mode_invalid_mode() -> None:
    """Test that invalid mode exits."""
    with pytest.raises(SystemExit):
        toggle_mode("invalid", "proj", "region", "svc")


def test_toggle_mode_dev_without_url() -> None:
    """Test that dev mode without URL exits."""
    with pytest.raises(SystemExit):
        toggle_mode("dev", "proj", "region", "svc", forward_url=None)


def test_toggle_mode_dev() -> None:
    """Test switching to dev mode."""
    env_before = {"MODE": "prod"}
    env_after = {"MODE": "dev", "FORWARD_URL": "https://example.ngrok.io"}
    side_effects = [env_before, env_after]
    with (
        patch("src.cli.toggle_mode.get_current_mode", side_effect=side_effects),
        patch("src.cli.toggle_mode.run_command") as mock_run,
    ):
        toggle_mode(
            "dev", "proj", "region", "svc", forward_url="https://example.ngrok.io"
        )
    mock_run.assert_called_once()


def test_toggle_mode_prod() -> None:
    """Test switching to prod mode."""
    env_before = {"MODE": "dev"}
    env_after = {"MODE": "prod"}
    side_effects = [env_before, env_after]
    with (
        patch("src.cli.toggle_mode.get_current_mode", side_effect=side_effects),
        patch("src.cli.toggle_mode.run_command") as mock_run,
    ):
        toggle_mode("prod", "proj", "region", "svc")
    mock_run.assert_called_once()


def test_main_missing_project(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test that missing --project exits."""
    monkeypatch.delenv("GCP_PROJECT_ID", raising=False)
    with (
        patch("sys.argv", ["toggle-mode", "prod"]),
        pytest.raises(SystemExit),
    ):
        main()


def test_main_dev_mode(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test main() in dev mode."""
    monkeypatch.setenv("GCP_PROJECT_ID", "my-proj")
    with (
        patch("sys.argv", ["toggle-mode", "dev", "--url", "https://example.ngrok.io"]),
        patch("src.cli.toggle_mode.toggle_mode") as mock_toggle,
    ):
        main()
    mock_toggle.assert_called_once_with(
        mode="dev",
        project_id="my-proj",
        region="asia-northeast1",
        service_name="discord-gateway",
        forward_url="https://example.ngrok.io",
    )


def test_main_prod_mode(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test main() in prod mode."""
    monkeypatch.setenv("GCP_PROJECT_ID", "my-proj")
    with (
        patch("sys.argv", ["toggle-mode", "prod"]),
        patch("src.cli.toggle_mode.toggle_mode") as mock_toggle,
    ):
        main()
    mock_toggle.assert_called_once_with(
        mode="prod",
        project_id="my-proj",
        region="asia-northeast1",
        service_name="discord-gateway",
        forward_url=None,
    )


# --- register_commands main() tests ---


def test_register_commands_main_success() -> None:
    """Test that main() calls register_commands."""
    with (
        patch("sys.argv", ["register-commands"]),
        patch("src.cli.register_commands.register_commands") as mock_register,
    ):
        register_commands_main()
    mock_register.assert_called_once()


def test_register_commands_main_failure_exits() -> None:
    """Test that main() exits on error."""
    with (
        patch("sys.argv", ["register-commands"]),
        patch(
            "src.cli.register_commands.register_commands",
            side_effect=RuntimeError("fail"),
        ),
        pytest.raises(SystemExit),
    ):
        register_commands_main()
