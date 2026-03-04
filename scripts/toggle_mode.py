#!/usr/bin/env python3
"""Cloud Run モード切替スクリプト

Cloud Run の環境変数を更新して、prod/dev モードを切り替える。
dev モードでは FORWARD_URL を設定し、prod モードでは MODE=prod に戻す。
"""

import argparse
import json
import os
import subprocess
import sys


def run_command(cmd: list[str], capture_output: bool = False) -> subprocess.CompletedProcess:
    """Run a shell command and handle errors."""
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(
        cmd,
        capture_output=capture_output,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        print(f"Error: Command failed with exit code {result.returncode}", file=sys.stderr)
        if result.stderr:
            print(result.stderr, file=sys.stderr)
        sys.exit(1)
    return result


def get_current_mode(project_id: str, region: str, service_name: str) -> dict[str, str]:
    """Get current environment variables from Cloud Run service."""
    cmd = [
        "gcloud",
        "run",
        "services",
        "describe",
        service_name,
        f"--project={project_id}",
        f"--region={region}",
        "--format=json",
    ]
    result = run_command(cmd, capture_output=True)
    service_data = json.loads(result.stdout)

    env_vars = {}
    if "spec" in service_data and "template" in service_data["spec"]:
        containers = service_data["spec"]["template"]["spec"]["containers"]
        if containers and "env" in containers[0]:
            for env in containers[0]["env"]:
                env_vars[env["name"]] = env.get("value", "")

    return env_vars


def toggle_mode(
    mode: str,
    project_id: str,
    region: str,
    service_name: str,
    forward_url: str | None = None,
) -> None:
    """Toggle Cloud Run service mode."""
    if mode not in ["prod", "dev"]:
        print("Error: mode must be 'prod' or 'dev'", file=sys.stderr)
        sys.exit(1)

    if mode == "dev" and not forward_url:
        print("Error: --url is required when switching to dev mode", file=sys.stderr)
        sys.exit(1)

    print(f"\n🔄 Switching Cloud Run service to {mode.upper()} mode...")
    print(f"   Project: {project_id}")
    print(f"   Region: {region}")
    print(f"   Service: {service_name}")

    # Get current environment variables
    current_env = get_current_mode(project_id, region, service_name)
    print(f"\nℹ️  Current MODE: {current_env.get('MODE', 'not set')}")

    # Build update command
    cmd = [
        "gcloud",
        "run",
        "services",
        "update",
        service_name,
        f"--project={project_id}",
        f"--region={region}",
    ]

    if mode == "dev":
        print(f"   Forward URL: {forward_url}")
        cmd.append(f"--update-env-vars=MODE=dev,FORWARD_URL={forward_url}")
    else:  # prod
        cmd.append("--update-env-vars=MODE=prod")
        cmd.append("--remove-env-vars=FORWARD_URL")

    # Execute update
    run_command(cmd)

    # Verify the change
    print("\n✅ Mode switch complete!")
    new_env = get_current_mode(project_id, region, service_name)
    print(f"   New MODE: {new_env.get('MODE', 'not set')}")
    if mode == "dev":
        print(f"   FORWARD_URL: {new_env.get('FORWARD_URL', 'not set')}")

    print("\n⚠️  Note: It may take ~30 seconds for the new revision to become active.")


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Toggle Cloud Run service between prod and dev modes"
    )
    parser.add_argument(
        "mode",
        choices=["prod", "dev"],
        help="Target mode (prod or dev)",
    )
    parser.add_argument(
        "--url",
        help="Forward URL for dev mode (required when mode=dev)",
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
        print("Error: --project or GCP_PROJECT_ID environment variable required", file=sys.stderr)
        sys.exit(1)

    toggle_mode(
        mode=args.mode,
        project_id=args.project,
        region=args.region,
        service_name=args.service,
        forward_url=args.url,
    )


if __name__ == "__main__":
    main()
