# Discord Service Gateway

Discordからのスラッシュコマンドを受け取り、n8nや他のWebサービスをコントロールするための基盤です。

## 開発環境のセットアップ

1.  **依存関係のインストール**
    ```bash
    uv sync
    ```

2.  **環境変数の設定**
    `.env.example` を `.env` にコピーし、Discord Developer Portal から取得した値を設定します。
    ```bash
    cp .env.example .env
    ```

3.  **サーバーの起動**
    ```bash
    uv run python src/main.py
    ```

## Docker Compose による開発環境の起動（推奨）

FastAPI と ngrok を一括起動できます。事前に Docker および Docker Compose が必要です。

1.  **環境変数の設定**
    `.env` に ngrok の認証情報を追加します。
    ```
    NGROK_AUTHTOKEN=your_ngrok_authtoken_here
    NGROK_DOMAIN=your_ngrok_domain_here
    ```

2.  **起動**
    ```bash
    docker compose up
    ```
    `app` コンテナ（FastAPI）と `ngrok` コンテナが起動します。ngrok の管理画面は `http://localhost:4040` で確認できます。

3.  **ホットリロード**
    `src/` 配下のファイルを編集すると、コンテナを再起動せずにサーバーが自動リロードされます。

## Discord との疎通確認 (ngrok)

### Docker Compose 使用時

`NGROK_DOMAIN` に設定した静的ドメインが ngrok の公開 URL になります。

### ローカル実行時

1.  **ngrok の起動**
    サーバーが起動しているポート（デフォルト: 8000）を外部に公開します。
    ```bash
    ngrok http 8000
    ```

2.  **Discord Developer Portal の設定**
    - アプリケーションを選択し、"General Information" ページの "INTERACTIONS ENDPOINT URL" に、ngrok の URL（例: `https://xxxx.ngrok-free.app/interactions`）を入力して保存します。
    - 保存時に Discord から PING リクエストが送信され、署名検証が正しく行われていれば保存が完了します。

## Cloud Run を経由したローカル開発（プロキシモード）

Discord の Interaction Endpoint URL を Cloud Run に固定したまま、リクエストをローカル環境に転送してデバッグできます。

### 前提条件

- `scripts/setup_gcp.sh` を実行済みで、GitHub Secrets が登録されていること
- Cloud Run に最新版がデプロイされていること（`git tag` でデプロイ）
- `.env` に以下の GCP 設定が追加されていること

```
GCP_PROJECT_ID=your-project-id
GCP_REGION=asia-northeast1
GCP_SERVICE_NAME=discord-gateway
NGROK_DOMAIN=your-domain.ngrok-free.app
```

### 起動（dev モードに自動切替）

```bash
./scripts/dev.sh up
```

このコマンドは以下を自動で実行します：

1. `docker compose up` でローカルコンテナ（FastAPI + ngrok）を起動
2. Cloud Run の `MODE` を `dev` に切り替え、`FORWARD_URL` に ngrok の URL を設定

```
Discord → Cloud Run（署名検証）→ ngrok → ローカル FastAPI
```

### 停止（prod モードに自動復帰）

```bash
./scripts/dev.sh down
```

1. Cloud Run の `MODE` を `prod` に戻す
2. `docker compose down` でローカルコンテナを停止

### 手動でのモード切替

`dev.sh` を使わずに手動で切り替えることもできます：

```bash
# dev モードに切替（ローカルに転送）
python3 scripts/toggle_mode.py dev --url https://your-domain.ngrok-free.app

# prod モードに戻す
python3 scripts/toggle_mode.py prod
```

> **注意**: `dev.sh down` を忘れると Cloud Run が `dev` モードのままになり、本番リクエストがローカルに転送されなくなります。万一の場合は上記の手動コマンドで復旧してください。

### 動作確認

ローカル起動後、Discord でコマンドを実行すると `docker compose logs -f app` にログが流れます：

```bash
./scripts/dev.sh logs -f
```

## 品質チェック

```bash
# Lint
uv run ruff check .

# Format check
uv run ruff format --check .

# Type check
uv run mypy .

# Test
uv run pytest
```
