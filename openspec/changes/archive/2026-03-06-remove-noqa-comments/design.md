## Context
現在、コードベース内の各所に `noqa` コメントが散在しており、Lint ルールを無視する理由がソースコード内に直接記述されています。これはコードのノイズとなり、またプロジェクト全体の Lint ポリシーの一貫性を損なっています。特に `print` の使用、テストコードでのアサートやモックトークン、例外処理の書き方などが主な要因です。

## Goals / Non-Goals

**Goals:**
- ソースコードからすべてのインライン `noqa` コメントを排除する。
- 正当な例外（CLI での `print` など）は `pyproject.toml` でディレクトリ/ファイル単位で一括管理する。
- 修正可能な不備（例外処理の不備など）はリファクタリングによって解消する。

**Non-Goals:**
- Lint ルール自体の緩和（ルールセットを減らすことはしない）。
- 大規模なアーキテクチャの変更。

## Decisions

### 1. pyproject.toml での `per-file-ignores` 活用
コンテキストに応じて正当な理由がある警告については、以下の通り `pyproject.toml` で一括管理します。
- `src/cli/**/*.py`: `T201` (print), `S603` (subprocess without shell) を許容。CLI ツールとしての性質上、これらは標準的な挙動であるため。
- `src/core/config.py`: `S105` (hardcoded password/token) を許容。デフォルト値としてダミートークンを設定する必要があるため。
- `src/main.py`: `S104` (bind to all interfaces) を許容。コンテナ環境（Cloud Run）での実行に `0.0.0.0` へのバインドが必要なため。
- `tests/**/*.py`: `S105` (hardcoded secret), `S101` (assert) 等を許容。テストコードの性質上、これらは不可欠であるため。

### 2. 例外処理のリファクタリング (TRY400, TRY003)
- **TRY400**: `logger.error` で例外オブジェクトを渡している箇所を `logger.exception` に変更し、スタックトレースを適切に出力するようにします。スタックトレースが不要な場合は `logger.warning` または `logger.error` を適切に使い分けます。
- **TRY003**: 長いエラーメッセージを伴う `raise RuntimeError` 等を避けるため、カスタム例外クラス（`src/core/exceptions.py`）を導入します。これにより、例外発生時のコードが簡潔になり、意図も明確になります。

### 3. noqa の一括削除
設定とリファクタリングの完了後、`grep` 等を用いてプロジェクト全域から `# noqa` コメントを削除します。

## Risks / Trade-offs

- [Risk] `per-file-ignores` で広範囲にルールを無視すると、本来検出すべきバグを見逃す可能性がある。
  - [Mitigation] 無視するルールを最小限（`T201`, `S105` 等）に絞り、ディレクトリ単位で限定的に適用することで影響を最小化します。
- [Risk] 大量のファイル変更が発生するため、コンフリクトの可能性がある。
  - [Mitigation] 本変更を短期間で完了させ、マージします。
