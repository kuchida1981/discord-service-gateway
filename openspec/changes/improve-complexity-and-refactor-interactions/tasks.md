# Tasks: リファクタリング作業手順

- [ ] **Phase 1: 環境整備**
  - [ ] `pyproject.toml` の `tool.ruff.lint.select` に `"C90"` を追加。
  - [ ] `ruff check .` を実行し、`C901` エラーが出ることを確認。

- [ ] **Phase 2: リファクタリング（転送ロジック）**
  - [ ] `src/api/routes.py` の転送ロジックを `_forward_to_dev` 関数に切り出す。
  - [ ] テストを実行し、開発モードの挙動が変わらないことを確認。

- [ ] **Phase 3: リファクタリング（コマンド処理）**
  - [ ] `src/api/handlers.py` を作成し、既存のコマンドロジックを移行。
  - [ ] `interactions` 関数にディスパッチロジックを実装。
  - [ ] `# noqa: PLR0911, PLR0912` を削除。

- [ ] **Phase 4: 最終検証**
  - [ ] `uv run ruff check .` がパスすることを確認。
  - [ ] `uv run pytest` がパスすることを確認（カバレッジ 100% 維持）。
