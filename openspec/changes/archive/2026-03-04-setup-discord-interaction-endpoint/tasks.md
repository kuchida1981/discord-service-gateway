## 1. Project Initialization

- [x] 1.1 `uv init` によるプロジェクトの初期化
- [x] 1.2 `pyproject.toml` への依存関係の追加 (fastapi, uvicorn, pynacl, pydantic-settings, httpx)
- [x] 1.3 `ruff`, `pytest`, `mypy` の設定ファイル (.ruff.toml, pyproject.toml内の設定等) の作成
- [x] 1.4 ディレクトリ構造 (`src/`, `tests/`) の作成

## 2. Configuration & Core Logic

- [x] 2.1 `src/core/config.py` の作成 (DISCORD_PUBLIC_KEY 等の環境変数管理)
- [x] 2.2 `.env.example` の作成と `.env` の `.gitignore` への追加確認
- [x] 2.3 `src/api/deps.py` に ED25519 署名検証ロジックを実装

## 3. API Implementation

- [x] 3.1 `src/api/routes.py` に `/` (Health Check) と `/interactions` エンドポイントを定義
- [x] 3.2 `/interactions` で Discord の `PING` (Type 1) に対する `PONG` レスポンスを実装
- [x] 3.3 `src/main.py` で FastAPI アプリを初期化し、ルーターを接続

## 4. Verification & Testing

- [x] 4.1 `tests/test_main.py` に `/` エンドポイントのテストを実装
- [x] 4.2 `tests/test_interactions.py` に署名検証と `PING/PONG` のテストを実装
- [x] 4.3 `ngrok` を使用したローカルサーバーの公開と Discord Developer Portal での URL 検証
