"""Tests for CLI tools."""

import json
import subprocess
from pathlib import Path
from unittest.mock import MagicMock, patch

import httpx
import pytest

from src.cli.register_commands import main as register_commands_main
from src.cli.register_commands import register_commands
from src.cli.toggle_mode import (
    GcpConfig,
    get_current_mode,
    load_env_file,
    main,
    run_command,
    show_status,
    toggle_mode,
)
from src.core.exceptions import ConfigurationError

_GCP = GcpConfig(project_id="proj", region="region", service_name="svc")
_MAIN_GCP = GcpConfig("my-proj", "asia-northeast1", "discord-gateway")

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
        mock_settings.DISCORD_TOKEN = "token123"
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
        mock_settings.DISCORD_TOKEN = "token123"
        mock_settings.DISCORD_GUILD_ID = None
        register_commands()

    called_url = mock_put.call_args[0][0]
    assert "/guilds/" not in called_url


def test_register_commands_raises_when_token_missing() -> None:
    """Test that missing DISCORD_TOKEN raises ConfigurationError."""
    with patch("src.cli.register_commands.settings") as mock_settings:
        mock_settings.DISCORD_TOKEN = "dummy_token"
        mock_settings.DISCORD_APPLICATION_ID = "app123"
        mock_settings.DISCORD_GUILD_ID = None
        with pytest.raises(ConfigurationError):
            register_commands()


def test_register_commands_raises_when_app_id_missing() -> None:
    """Test that missing DISCORD_APPLICATION_ID raises ConfigurationError."""
    with patch("src.cli.register_commands.settings") as mock_settings:
        mock_settings.DISCORD_TOKEN = "real_token"
        mock_settings.DISCORD_APPLICATION_ID = "dummy_app_id"
        mock_settings.DISCORD_GUILD_ID = None
        with pytest.raises(ConfigurationError):
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
        mock_settings.DISCORD_TOKEN = "real_token"
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
        mock_settings.DISCORD_TOKEN = "real_token"
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
        env = get_current_mode(_GCP)
    assert env["MODE"] == "prod"


def test_get_current_mode_empty_containers() -> None:
    """Test get_current_mode when spec has no containers."""
    service_json: dict[str, object] = {
        "spec": {"template": {"spec": {"containers": []}}}
    }
    mock_result = _make_proc(0, stdout=json.dumps(service_json))
    with patch("src.cli.toggle_mode.run_command", return_value=mock_result):
        env = get_current_mode(_GCP)
    assert env == {}


def test_get_current_mode_no_spec() -> None:
    """Test get_current_mode when service data has no spec."""
    mock_result = _make_proc(0, stdout=json.dumps({}))
    with patch("src.cli.toggle_mode.run_command", return_value=mock_result):
        env = get_current_mode(_GCP)
    assert env == {}


def test_get_current_mode_partial_spec() -> None:
    """Test get_current_mode with a partially complete spec (missing inner spec key)."""
    service_json: dict[str, object] = {"spec": {"template": {}}}
    mock_result = _make_proc(0, stdout=json.dumps(service_json))
    with patch("src.cli.toggle_mode.run_command", return_value=mock_result):
        env = get_current_mode(_GCP)
    assert env == {}


def test_toggle_mode_invalid_mode() -> None:
    """Test that invalid mode exits."""
    with pytest.raises(SystemExit):
        toggle_mode("invalid", _GCP)


def test_toggle_mode_dev_without_url() -> None:
    """Test that dev mode without URL exits."""
    with (
        patch("src.cli.toggle_mode.get_current_mode", return_value={"MODE": "prod"}),
        pytest.raises(SystemExit),
    ):
        toggle_mode("dev", _GCP, forward_url=None)


def test_toggle_mode_dev() -> None:
    """Test switching to dev mode."""
    env_before = {"MODE": "prod"}
    env_after = {"MODE": "dev", "FORWARD_URL": "https://example.ngrok.io"}
    side_effects = [env_before, env_after]
    with (
        patch("src.cli.toggle_mode.get_current_mode", side_effect=side_effects),
        patch("src.cli.toggle_mode.run_command") as mock_run,
    ):
        toggle_mode("dev", _GCP, forward_url="https://example.ngrok.io")
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
        toggle_mode("prod", _GCP)
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
    call = mock_toggle.call_args
    assert call.kwargs["mode"] == "dev"
    assert call.kwargs["gcp"] == _MAIN_GCP
    assert call.kwargs["forward_url"] == "https://example.ngrok.io"
    assert call.kwargs["sync"] is False


def test_main_dev_mode_with_sync(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test main() in dev mode with --sync flag."""
    monkeypatch.setenv("GCP_PROJECT_ID", "my-proj")
    with (
        patch(
            "sys.argv",
            ["toggle-mode", "dev", "--url", "https://example.ngrok.io", "--sync"],
        ),
        patch("src.cli.toggle_mode.toggle_mode") as mock_toggle,
    ):
        main()
    call = mock_toggle.call_args
    assert call.kwargs["sync"] is True
    assert call.kwargs["gcp"] == _MAIN_GCP


def test_main_prod_mode(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test main() in prod mode."""
    monkeypatch.setenv("GCP_PROJECT_ID", "my-proj")
    with (
        patch("sys.argv", ["toggle-mode", "prod"]),
        patch("src.cli.toggle_mode.toggle_mode") as mock_toggle,
    ):
        main()
    call = mock_toggle.call_args
    assert call.kwargs["mode"] == "prod"
    assert call.kwargs["gcp"] == _MAIN_GCP
    assert call.kwargs["forward_url"] is None
    assert call.kwargs["sync"] is False


def test_main_status_mode(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test main() in status mode."""
    monkeypatch.setenv("GCP_PROJECT_ID", "my-proj")
    monkeypatch.delenv("NGROK_DOMAIN", raising=False)
    with (
        patch("sys.argv", ["toggle-mode", "status"]),
        patch("src.cli.toggle_mode.show_status") as mock_status,
    ):
        main()
    call = mock_status.call_args
    assert call.kwargs["gcp"] == _MAIN_GCP
    assert call.kwargs["ngrok_domain"] is None


def test_load_env_file_parses_correctly(tmp_path: Path) -> None:
    """Test that load_env_file correctly parses a .env file."""
    env_file = tmp_path / ".env"
    env_file.write_text("KEY1=value1\n# comment\nKEY2=value2\n\nKEY3=\n")
    result = load_env_file(str(env_file))
    assert result == {"KEY1": "value1", "KEY2": "value2", "KEY3": ""}


def test_load_env_file_missing_returns_empty(tmp_path: Path) -> None:
    """Test that load_env_file returns empty dict for missing file."""
    result = load_env_file(str(tmp_path / "nonexistent.env"))
    assert result == {}


def test_show_status_no_env_file() -> None:
    """Test show_status when no .env file exists and no ngrok domain."""
    cloud_env = {"MODE": "dev", "FORWARD_URL": "https://example.ngrok.io"}
    with patch("src.cli.toggle_mode.get_current_mode", return_value=cloud_env):
        show_status(gcp=_GCP, ngrok_domain=None, env_file="/nonexistent/.env")


def test_show_status_with_env_file(tmp_path: Path) -> None:
    """Test show_status when .env file exists, comparing local vs Cloud Run vars."""
    env_file = tmp_path / ".env"
    env_file.write_text(
        "DISCORD_PUBLIC_KEY=localkey\n"
        "PROXY_SECRET=secret\n"
        "N8N_HEALTH_URL=https://n8n.example.com/healthz\n"
    )
    cloud_env = {
        "MODE": "dev",
        "FORWARD_URL": "https://example.ngrok.io",
        "DISCORD_PUBLIC_KEY": "cloudkey",
        "PROXY_SECRET": "secret",
    }
    with patch("src.cli.toggle_mode.get_current_mode", return_value=cloud_env):
        show_status(gcp=_GCP, ngrok_domain="example.ngrok.io", env_file=str(env_file))


def test_toggle_mode_dev_with_sync(tmp_path: Path) -> None:
    """Test toggle_mode in dev mode with --sync syncs SYNC_ENV_VARS."""
    env_file = tmp_path / ".env"
    env_file.write_text("DISCORD_PUBLIC_KEY=mykey\nPROXY_SECRET=mysecret\n")
    env_before = {"MODE": "prod"}
    env_after = {"MODE": "dev", "FORWARD_URL": "https://example.ngrok.io"}
    with (
        patch(
            "src.cli.toggle_mode.get_current_mode",
            side_effect=[env_before, env_after],
        ),
        patch("src.cli.toggle_mode.run_command") as mock_run,
    ):
        toggle_mode(
            "dev",
            _GCP,
            forward_url="https://example.ngrok.io",
            sync=True,
            env_file=str(env_file),
        )
    call_args = mock_run.call_args[0][0]
    update_arg = next(a for a in call_args if a.startswith("--update-env-vars="))
    assert "DISCORD_PUBLIC_KEY=mykey" in update_arg
    assert "PROXY_SECRET=mysecret" in update_arg


def test_toggle_mode_dev_escapes_commas_in_values(tmp_path: Path) -> None:
    """Test that commas in env var values are escaped to prevent injection."""
    env_file = tmp_path / ".env"
    # 値にカンマが含まれると gcloud が別の env var として解釈するため要エスケープ
    env_file.write_text("PROXY_SECRET=secret,INJECTED=bad\n")
    env_before = {"MODE": "prod"}
    env_after = {"MODE": "dev", "FORWARD_URL": "https://example.ngrok.io"}
    with (
        patch(
            "src.cli.toggle_mode.get_current_mode",
            side_effect=[env_before, env_after],
        ),
        patch("src.cli.toggle_mode.run_command") as mock_run,
    ):
        toggle_mode(
            "dev",
            _GCP,
            forward_url="https://example.ngrok.io",
            sync=True,
            env_file=str(env_file),
        )
    call_args = mock_run.call_args[0][0]
    update_arg = next(a for a in call_args if a.startswith("--update-env-vars="))
    # カンマが \, にエスケープされ、独立した env var として解釈されないこと
    assert "PROXY_SECRET=secret\\,INJECTED=bad" in update_arg


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
