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

```
Discord → Cloud Run（署名検証）→ ngrok → ローカル FastAPI
```

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

### ステータス確認

起動前に現在の接続・同期状況を確認できます：

```bash
./scripts/dev.sh status
```

以下の情報が表示されます：

- ローカルの ngrok URL
- Cloud Run 側の `MODE` と転送先 URL
- 同期対象の環境変数（`DISCORD_PUBLIC_KEY` 等）のローカル↔Cloud Run 比較

```
=== Development Environment Status ===
   Project: your-project-id
   Region: asia-northeast1
   Service: discord-gateway

ngrok URL: https://your-domain.ngrok-free.app

[Cloud Run]
   MODE:        prod
   FORWARD_URL: (not set)

[Sync Variables]
   VAR                            LOCAL                CLOUD RUN            STATUS
   ------------------------------ -------------------- -------------------- ------
   DISCORD_PUBLIC_KEY             abcd1234...          abcd1234...          OK
   PROXY_SECRET                   xxxxxxxx             xxxxxxxx             OK
   N8N_HEALTH_URL                 https://n8n...       https://n8n...       OK
```

`MISMATCH` が表示された場合は、`dev.sh up` で自動同期されます。

### 起動（dev モードに自動切替）

```bash
./scripts/dev.sh up
```

このコマンドは以下を自動で実行します：

1. `.env` と `.env.example` を比較し、不足している変数があれば警告
2. `.env` のハッシュ値（`ENV_HASH`）を算出して Docker に渡す（`.env` 変更時にコンテナを再作成）
3. `docker compose up` でローカルコンテナ（FastAPI + ngrok）を起動
4. Cloud Run の `MODE` を `dev` に切り替え、プロキシ動作に必要な環境変数を同期

### 停止（prod モードに自動復帰）

```bash
./scripts/dev.sh down
```

1. Cloud Run の `MODE` を `prod` に戻す
2. `docker compose down` でローカルコンテナを停止

> **注意**: `dev.sh down` を忘れると Cloud Run が `dev` モードのままになり、本番リクエストがローカルに転送されなくなります。万一の場合は `uv run toggle-mode prod` で手動復旧してください。

### ローカルで動作確認する手順（例）

**ゴール**: コマンドの挙動をローカルで変えて、Discord から動作確認する。

#### 1. `.env` に確認用の値を追加

```bash
# .env に追記
TEST_VALUE=hello-from-local
```

#### 2. ステータスを確認

```bash
./scripts/dev.sh status
```

Cloud Run が `prod` モードであることを確認します。

#### 3. ローカル起動

```bash
./scripts/dev.sh up
```

`.env` が変更されていれば Docker コンテナが再作成されます。Cloud Run が `dev` モードに切り替わり、`DISCORD_PUBLIC_KEY` 等が自動同期されます。

#### 4. Discord でコマンドを実行してログを確認

```bash
./scripts/dev.sh logs -f
```

Discord でコマンドを叩くと、ここにリクエストのログが流れます。

#### 5. `.env` を書き換えて再起動

```bash
# .env の値を変更
TEST_VALUE=updated-value

./scripts/dev.sh up  # ENV_HASH が変わるのでコンテナが自動再作成される
```

#### 6. 終了

```bash
./scripts/dev.sh down
```

### 環境変数の同期について

`dev.sh up` 時に Cloud Run へ自動同期される変数は `src/cli/toggle_mode.py` の `SYNC_ENV_VARS` で管理しています：

```python
SYNC_ENV_VARS = [
    "DISCORD_PUBLIC_KEY",
    "PROXY_SECRET",
    "N8N_HEALTH_URL",
]
```

Cloud Run に同期が必要な新しい変数を追加する場合は、このリストに追記してください。ローカルコンテナだけで使う変数（`.env` から Docker に渡されるもの）はここに追加不要です。

### 手動でのモード切替

`dev.sh` を使わずに手動で切り替えることもできます：

```bash
# dev モードに切替（環境変数も同期）
uv run toggle-mode dev --url https://your-domain.ngrok-free.app --sync

# 現在のステータスを確認
uv run toggle-mode status

# prod モードに戻す
uv run toggle-mode prod
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
