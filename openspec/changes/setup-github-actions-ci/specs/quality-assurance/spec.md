## MODIFIED Requirements

### Requirement: Static Code Analysis and Formatting
Ruffを使用して、コードの静的解析とフォーマットの一貫性を保たなければならない (SHALL)。
追加のルール（D, ANN, PT, PL, TRY等）を適用し、インポート順序、ドキュメント、型アノテーションを厳格にチェックしなければならない。
本チェックは、GitHub Actions の CI パイプライン上でも自動的に検証されなければならない (SHALL)。

#### Scenario: Running strict lint checks
- **WHEN** `ruff check .` コマンドを実行する、あるいは CI ジョブが実行される
- **THEN** 新しく追加されたルール（D, ANN等）に違反するコードが検出されてはならない

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
