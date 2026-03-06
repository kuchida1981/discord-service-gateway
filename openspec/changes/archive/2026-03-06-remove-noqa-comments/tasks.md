## 1. 設定の整理

- [x] 1.1 `pyproject.toml` の `[tool.ruff.lint.per-file-ignores]` セクションを更新し、ディレクトリ/ファイルごとの Lint 緩和ルールを追加する。

## 2. コードのリファクタリング

- [x] 2.1 `src/core/exceptions.py` を作成し、プロジェクト共通のカスタム例外クラス（`ConfigurationError` 等）を定義する。
- [x] 2.2 `src/cli/register_commands.py` において、長大な例外メッセージをカスタム例外の使用に置き換える (`TRY003`)。
- [x] 2.3 `src/cli/register_commands.py` の `except` ブロック内における `logger.error` を `logger.exception` または適切なログレベルに統合する (`TRY400`)。
- [x] 2.4 `src/api/deps.py` の署名検証失敗時における `logger.error` を `logger.warning` または `logger.exception` に適切に変更する (`TRY400`)。

## 3. noqa コメントの削除

- [x] 3.1 プロジェクト全域のソースコードおよびテストコードから `# noqa` コメントを一括削除する。

## 4. 動作検証

- [x] 4.1 `ruff check .` を実行し、すべての Lint エラーおよび警告が解消されていることを確認する。
- [x] 4.2 `pytest` を実行し、リファクタリングによって既存の機能に影響が出ていないことを確認する。
