## Purpose

プロジェクトのコード品質、堅牢性、および挙動を確実に担保するための静的解析とテストの仕様を定義する。
本仕様は、Ruffによる高速なLintとフォーマット、Pytestによる包括的な自動テスト、およびMypyによる静的型チェックを組み合わせ、
開発サイクル全体を通じて一貫した品質基準を維持することを目的としている。
## Requirements
### Requirement: Static Code Analysis and Formatting
Ruffを使用して、コードの静的解析とフォーマットの一貫性を保たなければならない (SHALL)。
追加のルール（D, ANN, PT, PL, TRY, C90等）を適用し、インポート順序、ドキュメント、型アノテーション、および循環的複雑度を厳格にチェックしなければならない。
本チェックは、GitHub Actions の CI パイプライン上でも自動的に検証されなければならない (SHALL)。

#### Scenario: Running strict lint checks
- **WHEN** `ruff check .` コマンドを実行する、あるいは CI ジョブが実行される
- **THEN** 新しく追加されたルール（D, ANN, C90等）に違反するコードが検出されてはならない

#### Scenario: Cyclomatic complexity enforcement
- **WHEN** `ruff check .` コマンドを実行する、あるいは CI ジョブが実行される
- **THEN** 循環的複雑度が閾値（10）を超える関数が検出されてはならない（C901）

#### Scenario: Running format checks
- **WHEN** `ruff format --check .` コマンドを実行する、あるいは CI ジョブが実行される
- **THEN** コードのフォーマットがプロジェクトの規定（.ruff.toml）に適合していることを確認しなければならない

### Requirement: Automated Testing
Pytestを使用して、APIエンドポイントの動作が期待通りであることを検証しなければならない (SHALL)。
すべてのテストがパスし、かつテストカバレッジが100%に達していなければならない。
本テストは、GitHub Actions の CI パイプライン上で自動的に実行されなければならない (SHALL)。

#### Scenario: Run API unit tests with coverage enforcement
- **WHEN** `pytest --cov=src --cov-report=term-missing --cov-fail-under=100` コマンドを実行する、あるいは CI ジョブが実行される
- **THEN** すべてのテストがパスし、かつカバレッジが100%に達していなければならない

### Requirement: Static Type Checking
Mypyを使用して、型定義の不整合を検出しなければならない (SHALL)。
本チェックは、GitHub Actions の CI パイプライン上でも自動的に検証されなければならない (SHALL)。

#### Scenario: Running type checks
- **WHEN** `mypy .` コマンドを実行する、あるいは CI ジョブが実行される
- **THEN** 関数の引数や戻り値の型不整合が検出されてはならない

### Requirement: Logging and Print Prevention
すべての `print` 関数の使用を禁止し、標準の `logging` モジュールを使用してログを出力しなければならない (SHALL)。

#### Scenario: Verify print removal
- **WHEN** コードベース内で `print(` を検索する
- **THEN** 実装コードおよびスクリプト内で `print` 関数の呼び出しが見つかってはならない

### Requirement: Draft Pull Request Control
CI リソースを最適化し、開発初期段階の不要な失敗を避けるため、Draft 状態の PR では特定の品質チェックをスキップしなければならない (SHALL)。
Ready for Review に切り替わった際に、自動的にすべてのチェックがトリガーされなければならない。

#### Scenario: Skip quality checks for Draft PR
- **WHEN** PR のステータスが `draft` である
- **THEN** `check-pr-issue` 以外の品質チェック（Lint, Test, TypeCheck, OpenSpec, TODO）は実行されてはならない

#### Scenario: Trigger all checks on Ready for Review
- **WHEN** PR のステータスが `Ready for Review` に変更される
- **THEN** スキップされていたすべての品質チェックが自動的にトリガーされなければならない

