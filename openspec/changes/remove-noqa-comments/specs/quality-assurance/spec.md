## MODIFIED Requirements

### Requirement: Static Code Analysis and Formatting
Ruffを使用して、コードの静的解析とフォーマットの一貫性を保たなければならない (SHALL)。
追加のルール（D, ANN, PT, PL, TRY, C90等）を適用し、インポート順序、ドキュメント、型アノテーション、および循環的複雑度を厳格にチェックしなければならない。
本チェックは、GitHub Actions の CI パイプライン上でも自動的に検証されなければならない (SHALL)。
プロジェクト全体で一貫したポリシーを適用するため、個別のソースコード行に `noqa` コメントを記述してルールを回避することを禁止し (SHALL)、
コンテキストに応じた例外（例: CLIツールでの `print` 許容等）はすべてプロジェクトの設定ファイル（`pyproject.toml`）の `per-file-ignores` セクションで一括管理しなければならない。

#### Scenario: Running strict lint checks
- **WHEN** `ruff check .` コマンドを実行する、あるいは CI ジョブが実行される
- **THEN** 新しく追加されたルール（D, ANN, C90等）に違反するコードが検出されてはならない

#### Scenario: No inline noqa comments
- **WHEN** ソースコード内で `# noqa` という文字列を検索する
- **THEN** ヒットする箇所が存在してはならない

#### Scenario: Centralized configuration for exceptions
- **WHEN** 特定のファイルやディレクトリに対して Lint ルールを適用しない必要がある場合
- **THEN** `pyproject.toml` の `per-file-ignores` セクションで設定を定義しなければならない

### Requirement: Logging and Print Prevention
プロダクションコードにおいては、すべての `print` 関数の使用を禁止し、標準の `logging` モジュールを使用してログを出力しなければならない (SHALL)。
ただし、CLI ツール（`src/cli/` 配下）など、標準出力がユーザーインターフェースの一部として機能するスクリプトにおいては、`print` 関数の使用を許容する (MAY)。
この例外は `pyproject.toml` の設定によって、個別の `noqa` なしに実現されなければならない。

#### Scenario: Verify print removal in production code
- **WHEN** `src/cli/` 以外のディレクトリ内で `print(` を検索する
- **THEN** 実装コード内で `print` 関数の呼び出しが見つかってはならない

#### Scenario: Allow print in CLI tools
- **WHEN** `src/cli/` 配下のスクリプトで `print` を使用している
- **THEN** Ruff のチェックがパスし、かつインラインの `noqa: T201` が存在しないことを確認する

### Requirement: Proper Exception Handling
例外処理においてエラーログを出力する場合、スタックトレースが必要な場合は `logger.exception` を使用し、不要な場合は `logger.warning` または `logger.error` を適切に使い分けなければならない (SHALL)。
`logger.error` のメッセージ内に単に例外オブジェクトを埋め込むことで、スタックトレースを伴わずに例外を報告する曖昧な実装を避ける。

#### Scenario: Using logger.exception in except block
- **WHEN** `except` ブロック内でエラーを報告する必要がある
- **THEN** `logger.exception` を使用してスタックトレースを出力するか、適切なメッセージで `logger.warning` / `logger.error` を使用し、不必要な `noqa: TRY400` が存在してはならない
