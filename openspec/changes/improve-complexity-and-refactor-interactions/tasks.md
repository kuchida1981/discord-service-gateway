# Tasks: リファクタリング作業手順

- [x] **Phase 1: 環境整備**
  - [x] `pyproject.toml` の `tool.ruff.lint.select` に `"C90"` を追加。
  - [x] `ruff check .` を実行し、`C901` エラーが出ることを確認。

- [x] **Phase 2: リファクタリング（転送ロジック）**
  - [x] `src/api/routes.py` の転送ロジックを `_forward_to_dev` 関数に切り出す。
  - [x] テストを実行し、開発モードの挙動が変わらないことを確認。

- [x] **Phase 3: リファクタリング（コマンド処理）**
  - [x] `src/api/handlers.py` を作成し、既存のコマンドロジックを移行。
  - [x] `interactions` 関数にディスパッチロジックを実装。
  - [x] `# noqa: PLR0911, PLR0912` を削除。

- [x] **Phase 4: 最終検証**
  - [x] `uv run ruff check .` がパスすることを確認。
  - [x] `uv run pytest` がパスすることを確認（カバレッジ 100% 維持）。
