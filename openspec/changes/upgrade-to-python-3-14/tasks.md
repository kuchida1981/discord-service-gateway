## 1. 構成ファイルの更新

- [x] 1.1 `.python-version` を `3.14` に更新
- [x] 1.2 `pyproject.toml` の `requires-python` を `">=3.14"` に更新
- [x] 1.3 `pyproject.toml` の `tool.ruff.target-version` を `"py314"` に更新
- [x] 1.4 `pyproject.toml` の `tool.mypy.python_version` を `"3.14"` に更新

## 2. 依存関係の更新

- [x] 2.1 `uv lock --upgrade` を実行して `uv.lock` を Python 3.14 向けに更新
- [x] 2.2 `uv sync` を実行してローカル環境を 3.14 に同期

## 3. コンテナおよび CI/CD の更新

- [x] 3.1 `Dockerfile` のベースイメージを `ghcr.io/astral-sh/uv:python3.14-bookworm-slim` に更新
- [x] 3.2 `.github/workflows/python-checks.yaml` 等の CI 設定に影響がないか確認

## 4. 検証とビルド

- [x] 4.1 `uv run ruff check .` を実行し、Lint エラーがないことを確認
- [x] 4.2 `uv run mypy .` を実行し、型チェックがパスすることを確認
- [x] 4.3 `uv run pytest` を実行し、全てのテストがパスすることを確認
- [x] 4.4 `docker build .` を実行し、イメージが正常にビルドできることを確認