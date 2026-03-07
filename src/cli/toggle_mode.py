#!/usr/bin/env python3
"""Cloud Run mode toggle script.

Updates Cloud Run environment variables to switch between prod/dev modes.
In dev mode, sets FORWARD_URL. In prod mode, restores MODE=prod.
"""

import argparse
import dataclasses
import json
import os
import subprocess
import sys
from pathlib import Path

# Environment variables synced to Cloud Run in dev mode
SYNC_ENV_VARS = [
    "DISCORD_PUBLIC_KEY",
    "PROXY_SECRET",
    "N8N_HEALTH_URL",
]

_DISPLAY_COL_WIDTH = 20


@dataclasses.dataclass
class GcpConfig:
    """GCP connection settings for Cloud Run operations."""

    project_id: str
    region: str
    service_name: str


def run_command(
    cmd: list[str], capture_output: bool = False
) -> subprocess.CompletedProcess[str]:
    """Run a shell command and handle errors."""
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(
        cmd,
        capture_output=capture_output,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        print(
            f"Error: Command failed with exit code {result.returncode}",
            file=sys.stderr,
        )
        if result.stderr:
            print(result.stderr, file=sys.stderr)
        sys.exit(1)
    return result


def load_env_file(env_path: str) -> dict[str, str]:
    """Load environment variables from a .env file."""
    env_vars: dict[str, str] = {}
    path = Path(env_path)
    if not path.exists():
        return env_vars
    with path.open() as f:
        for raw_line in f:
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                key, _, value = line.partition("=")
                env_vars[key.strip()] = value.strip()
    return env_vars


def get_current_mode(gcp: GcpConfig) -> dict[str, str]:
    """Get current environment variables from Cloud Run service."""
    cmd = [
        "gcloud",
        "run",
        "services",
        "describe",
        gcp.service_name,
        f"--project={gcp.project_id}",
        f"--region={gcp.region}",
        "--format=json",
    ]
    result = run_command(cmd, capture_output=True)
    service_data = json.loads(result.stdout)

    env_vars = {}
    template = service_data.get("spec", {}).get("template", {})
    containers = template.get("spec", {}).get("containers", [])
    if containers and "env" in containers[0]:
        for env in containers[0]["env"]:
            env_vars[env["name"]] = env.get("value", "")

    return env_vars


def toggle_mode(
    mode: str,
    gcp: GcpConfig,
    forward_url: str | None = None,
    sync: bool = False,
    env_file: str | None = None,
) -> None:
    """Toggle Cloud Run service mode."""
    if mode not in ["prod", "dev"]:
        print("Error: mode must be 'prod' or 'dev'", file=sys.stderr)
        sys.exit(1)

    if mode == "dev" and not forward_url:
        print("Error: --url is required when switching to dev mode", file=sys.stderr)
        sys.exit(1)

    print(f"\nSwitching Cloud Run service to {mode.upper()} mode...")
    print(f"   Project: {gcp.project_id}")
    print(f"   Region: {gcp.region}")
    print(f"   Service: {gcp.service_name}")

    current_env = get_current_mode(gcp)
    print(f"\nCurrent MODE: {current_env.get('MODE', 'not set')}")

    cmd = [
        "gcloud",
        "run",
        "services",
        "update",
        gcp.service_name,
        f"--project={gcp.project_id}",
        f"--region={gcp.region}",
    ]

    if mode == "dev":
        print(f"   Forward URL: {forward_url}")
        env_updates = ["MODE=dev", f"FORWARD_URL={forward_url}"]
        if sync and env_file:
            local_env = load_env_file(env_file)
            for var in SYNC_ENV_VARS:
                if var in local_env:
                    env_updates.append(f"{var}={local_env[var]}")
                    print(f"   Syncing {var} from local .env")
        cmd.append(f"--update-env-vars={','.join(env_updates)}")
    else:  # prod
        cmd.append("--update-env-vars=MODE=prod")
        cmd.append("--remove-env-vars=FORWARD_URL")

    run_command(cmd)

    print("\nMode switch complete!")
    new_env = get_current_mode(gcp)
    print(f"   New MODE: {new_env.get('MODE', 'not set')}")
    if mode == "dev":
        print(f"   FORWARD_URL: {new_env.get('FORWARD_URL', 'not set')}")

    print("\nNote: It may take ~30 seconds for the new revision to become active.")


def _truncate(val: str) -> str:
    """Truncate a string to fit in a display column."""
    if len(val) > _DISPLAY_COL_WIDTH:
        return val[: _DISPLAY_COL_WIDTH - 3] + "..."
    return val


def show_status(
    gcp: GcpConfig,
    ngrok_domain: str | None = None,
    env_file: str | None = None,
) -> None:
    """Show current development environment status."""
    print("\n=== Development Environment Status ===")
    print(f"   Project: {gcp.project_id}")
    print(f"   Region: {gcp.region}")
    print(f"   Service: {gcp.service_name}")

    if ngrok_domain:
        print(f"\nngrok URL: https://{ngrok_domain}")
    else:
        print("\nngrok URL: (NGROK_DOMAIN not set)")

    print("\n[Cloud Run]")
    cloud_env = get_current_mode(gcp)
    print(f"   MODE:        {cloud_env.get('MODE', 'not set')}")
    print(f"   FORWARD_URL: {cloud_env.get('FORWARD_URL', 'not set')}")

    if env_file and Path(env_file).exists():
        local_env = load_env_file(env_file)
        print("\n[Sync Variables]")
        print(f"   {'VAR':<30} {'LOCAL':<20} {'CLOUD RUN':<20} STATUS")
        print(f"   {'-' * 30} {'-' * 20} {'-' * 20} ------")
        for var in SYNC_ENV_VARS:
            local_val = local_env.get(var, "(not set)")
            cloud_val = cloud_env.get(var, "(not set)")
            status = "OK" if local_val == cloud_val else "MISMATCH"
            row = (
                f"   {var:<30} {_truncate(local_val):<20}"
                f" {_truncate(cloud_val):<20} {status}"
            )
            print(row)
    else:
        print("\n[Sync Variables] (no .env file found)")


def main() -> None:
    """Run the CLI entrypoint."""
    parser = argparse.ArgumentParser(
        description="Toggle Cloud Run service between prod and dev modes"
    )
    parser.add_argument(
        "mode",
        choices=["prod", "dev", "status"],
        help="Target mode (prod, dev, or status)",
    )
    parser.add_argument(
        "--url",
        help="Forward URL for dev mode (required when mode=dev)",
    )
    parser.add_argument(
        "--sync",
        action="store_true",
        help="Sync SYNC_ENV_VARS from local .env to Cloud Run (dev mode only)",
    )
    parser.add_argument(
        "--env-file",
        default=None,
        help="Path to .env file (default: .env in current directory)",
    )
    parser.add_argument(
        "--project",
        default=os.getenv("GCP_PROJECT_ID"),
        help="GCP Project ID (default: $GCP_PROJECT_ID)",
    )
    parser.add_argument(
        "--region",
        default=os.getenv("GCP_REGION", "asia-northeast1"),
        help="GCP Region (default: $GCP_REGION or asia-northeast1)",
    )
    parser.add_argument(
        "--service",
        default=os.getenv("GCP_SERVICE_NAME", "discord-gateway"),
        help="Cloud Run service name (default: $GCP_SERVICE_NAME or discord-gateway)",
    )

    args = parser.parse_args()

    if not args.project:
        print(
            "Error: --project or GCP_PROJECT_ID environment variable required",
            file=sys.stderr,
        )
        sys.exit(1)

    gcp = GcpConfig(
        project_id=args.project,
        region=args.region,
        service_name=args.service,
    )
    env_file = args.env_file or str(Path.cwd() / ".env")

    if args.mode == "status":
        show_status(
            gcp=gcp,
            ngrok_domain=os.getenv("NGROK_DOMAIN"),
            env_file=env_file,
        )
        return

    toggle_mode(
        mode=args.mode,
        gcp=gcp,
        forward_url=args.url,
        sync=args.sync,
        env_file=env_file,
    )


if __name__ == "__main__":  # pragma: no cover
    main()
