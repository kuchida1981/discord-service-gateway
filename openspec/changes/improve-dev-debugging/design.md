## Context

現在の開発環境起動プロセス（`dev.sh up`）は、プロキシ動作（Cloud Run 転送）を有効にするが、アプリの動作に必要な環境変数（例：`DISCORD_PUBLIC_KEY`）がローカルとクラウドで一致していることを保証していない。これにより、プロキシ経由でリクエストが届かない等のトラブルシューティングに時間を要している。

## Goals / Non-Goals

**Goals:**
- プロキシ動作に必須な環境変数のローカル・クラウド間での自動同期。
- ローカルの `.env` 変更を確実に Docker コンテナへ反映させる仕組みの導入。
- 現在の開発環境の「接続・同期ステータス」の可視化。

**Non-Goals:**
- データベース接続先やセンシティブなシークレット情報の無差別な同期。
- `docker-compose.yml` の大規模な構造変更。

## Decisions

### 1. 同期対象の明示的な管理
`src/cli/toggle_mode.py` に `SYNC_ENV_VARS` リストを定義し、同期対象（例：`DISCORD_PUBLIC_KEY`, `PROXY_SECRET`, `N8N_HEALTH_URL` 等）を限定する。これにより、意図しない設定の上書きを防ぐ。

### 2. 環境変数ハッシュによる Docker 再起動の強制
`dev.sh` 内で `.env` のハッシュ値を算出し、`export ENV_HASH=$(md5sum .env | cut -d' ' -f1)` を実行してから `docker compose up` を呼ぶ。`docker-compose.yml` の `labels` 等でこの変数を利用することで、`.env` が変更されると Docker がコンテナを「変更あり」とみなして再起動するようにする。

### 3. `dev.sh status` コマンドの追加
以下の情報を集約して表示する機能を `dev.sh` および `toggle_mode.py` に追加する。
- ローカルの ngrok URL
- Cloud Run 側の `MODE` と `FORWARD_URL`
- 同期対象変数の「一致・不一致」チェック

## Risks / Trade-offs

- **[Risk]** 同期漏れの発生 → **[Mitigation]** `dev.sh status` での比較表示により、不一致を検知可能にする。
- **[Risk]** 同期処理による `dev.sh up` の微増（`gcloud` 通信） → **[Mitigation]** `up` 時にのみ実行し、同期が必要な場合のみ警告・実行する等の工夫。
