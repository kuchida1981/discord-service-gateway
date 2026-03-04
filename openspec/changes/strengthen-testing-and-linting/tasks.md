## 1. 依存関係と設定の更新

- [ ] 1.1 `pytest-cov` を `pyproject.toml` の `dev-dependencies` (または `dependency-groups.dev`) に追加する
- [ ] 1.2 `pyproject.toml` の `tool.ruff` 設定を更新し、`D`, `ANN`, `PT`, `PL`, `TRY`, `TID` などのルールを有効にする
- [ ] 1.3 `pyproject.toml` に `tool.ruff.lint.per-file-ignores` を追加し、`tests/` 配下で `S101`, `PLR2004` を無視する設定を行う
- [ ] 1.4 `pyproject.toml` の `tool.pytest.ini_options` を更新し、`addopts = "--cov=src --cov-report=term-missing --cov-fail-under=100"` を追加する

## 2. 定数とEnumの導入

- [ ] 2.1 `src/core/constants.py` (新規) または適切な場所に Discord Interaction Type および Response Type の `Enum` を作成する
- [ ] 2.2 `src/api/routes.py` で使用されているマジックナンバーを、作成した `Enum` に置き換える

## 3. ロギングへの移行

- [ ] 3.1 `scripts/register_commands.py` の `print` 関数を `logging` に置き換える
- [ ] 3.2 `src/` 配下の残存している `print` 関数（あれば）を `logging` に置き換える

## 4. 既存のLintエラー修正

- [ ] 4.1 `ruff check . --fix` を実行し、自動修正可能なインポート順序（I001）などを解消する
- [ ] 4.2 残りのLintエラー（型アノテーションの不足、ドキュメント文字列の欠如など）を手動で修正する

## 5. テストの拡充とカバレッジ100%の達成

- [ ] 5.1 `uv run pytest` を実行し、現在のカバレッジを確認する
- [ ] 5.2 カバレッジが100%に満たない箇所を特定し、必要なテストケースを追加する
- [ ] 5.3 最終的に `ruff check .`, `mypy .`, `pytest` すべてがパスすることを確認する
