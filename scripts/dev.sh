#!/bin/bash
# Docker Compose ラッパースクリプト
# ローカル開発環境の起動・停止に連動して Cloud Run のモードを自動切替

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# .env ファイルを自動読み込み
if [[ -f "$PROJECT_ROOT/.env" ]]; then
  set -a
  source "$PROJECT_ROOT/.env"
  set +a
fi

# 色付きログ
info() { echo -e "\033[0;34m[INFO]\033[0m $*"; }
success() { echo -e "\033[0;32m[SUCCESS]\033[0m $*"; }
error() { echo -e "\033[0;31m[ERROR]\033[0m $*"; exit 1; }
warn() { echo -e "\033[0;33m[WARN]\033[0m $*"; }

# 使用方法
usage() {
    cat <<EOF
Usage: $0 <command> [options]

Commands:
  up      Start local development environment and switch Cloud Run to dev mode
  down    Stop local development environment and switch Cloud Run to prod mode
  restart Restart local environment (down + up)
  logs    Show docker compose logs
  status  Show current development environment and sync status

Options:
  --skip-cloud-run    Skip Cloud Run mode toggling (local-only mode)

Environment Variables (required for Cloud Run toggling):
  GCP_PROJECT_ID      GCP Project ID
  GCP_REGION          GCP Region (default: asia-northeast1)
  GCP_SERVICE_NAME    Cloud Run service name (default: discord-gateway)
  NGROK_DOMAIN        ngrok domain for forwarding (required for 'up')

Example:
  # Start with Cloud Run integration
  export GCP_PROJECT_ID=my-project
  export NGROK_DOMAIN=my-app.ngrok-free.app
  $0 up

  # Start without Cloud Run (local only)
  $0 up --skip-cloud-run

EOF
    exit 1
}

# .env と .env.example のキー比較バリデーション
validate_env_file() {
    local env_file="$PROJECT_ROOT/.env"
    local example_file="$PROJECT_ROOT/.env.example"

    if [[ ! -f "$example_file" ]]; then
        return 0
    fi

    if [[ ! -f "$env_file" ]]; then
        warn ".env file not found. Copy .env.example to get started."
        return 0
    fi

    local missing=()
    while IFS= read -r line; do
        [[ -z "$line" || "$line" =~ ^# ]] && continue
        local key="${line%%=*}"
        if [[ -n "$key" ]] && ! grep -q "^${key}=" "$env_file"; then
            missing+=("$key")
        fi
    done < "$example_file"

    if [[ ${#missing[@]} -gt 0 ]]; then
        warn "Missing environment variables in .env (defined in .env.example):"
        for var in "${missing[@]}"; do
            warn "  - $var"
        done
    fi
}

# .env の MD5 ハッシュを ENV_HASH としてエクスポート
compute_env_hash() {
    if [[ -f "$PROJECT_ROOT/.env" ]]; then
        export ENV_HASH
        ENV_HASH=$(md5sum "$PROJECT_ROOT/.env" | cut -d' ' -f1)
        info "ENV_HASH: $ENV_HASH"
    fi
}

# Cloud Run モード切替
toggle_cloud_run() {
    local mode=$1
    local forward_url=${2:-}

    if [[ "${SKIP_CLOUD_RUN:-false}" == "true" ]]; then
        info "Skipping Cloud Run mode toggle (--skip-cloud-run)"
        return 0
    fi

    if [[ -z "${GCP_PROJECT_ID:-}" ]]; then
        warn "GCP_PROJECT_ID not set - skipping Cloud Run mode toggle"
        warn "Set GCP_PROJECT_ID, GCP_REGION, and NGROK_DOMAIN to enable auto-toggling"
        return 0
    fi

    info "Toggling Cloud Run to $mode mode..."

    local cmd=("uv" "run" "toggle-mode" "$mode")
    [[ -n "$forward_url" ]] && cmd+=("--url" "$forward_url")
    [[ "$mode" == "dev" ]] && cmd+=("--sync")

    if "${cmd[@]}"; then
        success "Cloud Run mode switched to $mode"
    else
        error "Failed to toggle Cloud Run mode"
    fi
}

# ngrok URL の構築
get_ngrok_url() {
    local domain="${NGROK_DOMAIN:-}"
    if [[ -z "$domain" ]]; then
        error "NGROK_DOMAIN environment variable is required for 'up' command"
    fi
    echo "https://$domain"
}

# Docker Compose コマンド
cmd_up() {
    info "Starting local development environment..."

    # .env バリデーション
    validate_env_file

    # .env の変更を Docker コンテナに反映するためハッシュを算出
    compute_env_hash

    # docker compose up
    cd "$PROJECT_ROOT"
    docker compose up -d

    # Cloud Run を dev モードに切替（環境変数を同期）
    local ngrok_url
    ngrok_url=$(get_ngrok_url)
    toggle_cloud_run "dev" "$ngrok_url"

    success "Development environment is ready!"
    info ""
    info "Services:"
    info "  Local API: http://localhost:8000"
    info "  ngrok URL: $ngrok_url"
    info ""
    info "Cloud Run is now forwarding requests to your local environment."
    info "Use 'docker compose logs -f' to view logs."
}

cmd_down() {
    info "Stopping local development environment..."

    # Cloud Run を prod モードに戻す
    toggle_cloud_run "prod"

    # docker compose down
    cd "$PROJECT_ROOT"
    docker compose down

    success "Development environment stopped and Cloud Run restored to prod mode."
}

cmd_restart() {
    info "Restarting development environment..."
    cmd_down
    cmd_up
}

cmd_logs() {
    cd "$PROJECT_ROOT"
    docker compose logs "${@:2}"
}

cmd_status() {
    if [[ -z "${GCP_PROJECT_ID:-}" ]]; then
        warn "GCP_PROJECT_ID not set - cannot show Cloud Run status"
        return 0
    fi
    uv run toggle-mode status
}

# メイン処理
main() {
    if [[ $# -lt 1 ]]; then
        usage
    fi

    local command=$1
    shift

    # オプション解析
    while [[ $# -gt 0 ]]; do
        case $1 in
            --skip-cloud-run)
                export SKIP_CLOUD_RUN=true
                shift
                ;;
            -h|--help)
                usage
                ;;
            *)
                break
                ;;
        esac
    done

    case $command in
        up)
            cmd_up "$@"
            ;;
        down)
            cmd_down "$@"
            ;;
        restart)
            cmd_restart "$@"
            ;;
        logs)
            cmd_logs "$@"
            ;;
        status)
            cmd_status "$@"
            ;;
        -h|--help)
            usage
            ;;
        *)
            error "Unknown command: $command"
            usage
            ;;
    esac
}

main "$@"
