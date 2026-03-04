## 1. 環境設定の拡張

- [x] 1.1 `.env.example` に `NGROK_AUTHTOKEN` と `NGROK_DOMAIN` の項目を追加する
- [x] 1.2 `src/core/config.py` の `Settings` クラスに ngrok 関連の設定項目を追加する

## 2. Docker 構成の構築

- [x] 2.1 `ghcr.io/astral-sh/uv` をベースイメージとした開発用 `Dockerfile` を作成する
- [x] 2.2 `app` (FastAPI) と `ngrok` サービスを定義した `docker-compose.yml` を作成する
- [x] 2.3 `.dockerignore` を作成し、不要なファイル（`.venv`, `__pycache__` 等）を除外する

## 3. 動作検証

- [x] 3.1 `docker compose up` で両サービスが正常に起動することを確認する
- [x] 3.2 ソースコードの変更が検知され、コンテナ内のサーバーがリロードされることを確認する
- [x] 3.3 ngrok の公開 URL 経由で FastAPI の `/` (health check) にアクセスできることを確認する

## 4. 仕上げ

- [x] 4.1 `README.md` に Docker Compose を使用した開発環境の起動手順を追記する
- [x] 4.2 不要なデバッグ用プリントや一時的な設定が残っていないか確認する
