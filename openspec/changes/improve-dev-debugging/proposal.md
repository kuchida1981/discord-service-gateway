## Why

開発環境の起動（`dev.sh up`）において、ローカルの `.env` の変更が Cloud Run（プロキシ）や Docker コンテナに自動で反映されない。その結果、環境変数の追加・変更時にデバッグが困難になる問題（例：署名検証エラーの解消に時間がかかる）を解決するため。

## What Changes

- **Environment Sync**: `dev.sh up` 時にプロキシ動作に必要な環境変数（`DISCORD_PUBLIC_KEY`, `PROXY_SECRET` 等）をローカルから Cloud Run へ自動的に同期する。
- **Container Freshness**: `.env` の変更が確実に Docker コンテナに反映されるよう、`docker compose` の起動プロセスを改善する。
- **Configuration Validation**: `.env.example` との比較による環境変数の欠落検知。
- **Status Visibility**: 現在の接続先や同期状況を一覧表示する `dev.sh status` コマンドの導入。

## Capabilities

### New Capabilities
- なし

### Modified Capabilities
- `local-dev-automation`: 環境変数のクラウド同期、コンテナ反映保証、およびデバッグ可視化の要件を追加。
- `cli-tooling`: `dev.sh status` ツールおよび環境変数同期ツールの要件を追加。

## Impact

- `scripts/dev.sh` (ラッパースクリプト)
- `src/cli/toggle_mode.py` (Cloud Run 連携ロジック)
- `docker-compose.yml` (環境変数の参照方法など)
- 開発者のワークフロー（`dev.sh up` の挙動がより安全で確実になる）
