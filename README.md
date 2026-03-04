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

## Discord との疎通確認 (ngrok)

1.  **ngrok の起動**
    サーバーが起動しているポート（デフォルト: 8000）を外部に公開します。
    ```bash
    ngrok http 8000
    ```

2.  **Discord Developer Portal の設定**
    - アプリケーションを選択し、"General Information" ページの "INTERACTIONS ENDPOINT URL" に、ngrok の URL（例: `https://xxxx.ngrok-free.app/interactions`）を入力して保存します。
    - 保存時に Discord から PING リクエストが送信され、署名検証が正しく行われていれば保存が完了します。

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
