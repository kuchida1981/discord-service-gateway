## MODIFIED Requirements

### Requirement: Static Code Analysis and Formatting
Ruffを使用して、コードの静的解析とフォーマットの一貫性を保たなければならない (SHALL)。
追加のルール（D, ANN, PT, PL, TRY等）を適用し、インポート順序、ドキュメント、型アノテーションを厳格にチェックしなければならない。

#### Scenario: Running strict lint checks
- **WHEN** `ruff check .` コマンドを実行する
- **THEN** 新しく追加されたルール（D, ANN等）に違反するコードが検出されなければならない

#### Scenario: Running format checks
- **WHEN** `ruff format --check .` コマンドを実行する
- **THEN** コードのフォーマットがプロジェクトの規定（.ruff.toml）に適合していることを確認しなければならない

### Requirement: Automated Testing
Pytestを使用して、APIエンドポイントの動作が期待通りであることを検証しなければならない (SHALL)。
すべてのテストがパスし、かつテストカバレッジが100%に達していなければならない。

#### Scenario: Run API unit tests with coverage enforcement
- **WHEN** `pytest --cov=src --cov-report=term-missing --cov-fail-under=100` コマンドを実行する
- **THEN** すべてのテストがパスし、かつカバレッジが100%に達していなければならない

## ADDED Requirements

### Requirement: Logging and Print Prevention
すべての `print` 関数の使用を禁止し、標準の `logging` モジュールを使用してログを出力しなければならない (SHALL)。

#### Scenario: Verify print removal
- **WHEN** コードベース内で `print(` を検索する
- **THEN** 実装コードおよびスクリプト内で `print` 関数の呼び出しが見つかってはならない

### Requirement: Magic Value Elimination
プロトコル定数（Interaction Type等）やステータスコードを直接数値で記述することを禁止し、`Enum` または定数を使用しなければならない (SHALL)。

#### Scenario: Use Enum for Interaction Types
- **WHEN** `/interactions` エンドポイントの実装を確認する
- **THEN** `type == 1` のようなマジックナンバーではなく、`InteractionType.PING` のような Enum が使用されていなければならない
