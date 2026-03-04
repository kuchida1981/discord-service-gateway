## Purpose

プロジェクトのコード品質、堅牢性、および挙動を確実に担保するための静的解析とテストの仕様を定義する。
本仕様は、Ruffによる高速なLintとフォーマット、Pytestによる包括的な自動テスト、およびMypyによる静的型チェックを組み合わせ、
開発サイクル全体を通じて一貫した品質基準を維持することを目的としている。

## Requirements

### Requirement: Static Code Analysis and Formatting
Ruffを使用して、コードの静的解析とフォーマットの一貫性を保たなければならない (SHALL)。
追加のルール（D, ANN, PT, PL, TRY等）を適用し、インポート順序、ドキュメント、型アノテーションを厳格にチェックしなければならない。

#### Scenario: Running strict lint checks
- **WHEN** `ruff check .` コマンドを実行する
- **THEN** 新しく追加されたルール（D, ANN等）に違反するコードが検出されてはならない

#### Scenario: Running format checks
- **WHEN** `ruff format --check .` コマンドを実行する
- **THEN** コードのフォーマットがプロジェクトの規定（.ruff.toml）に適合していることを確認しなければならない

### Requirement: Automated Testing
Pytestを使用して、APIエンドポイントの動作が期待通りであることを検証しなければならない (SHALL)。
すべてのテストがパスし、かつテストカバレッジが100%に達していなければならない。

#### Scenario: Run API unit tests with coverage enforcement
- **WHEN** `pytest --cov=src --cov-report=term-missing --cov-fail-under=100` コマンドを実行する
- **THEN** すべてのテストがパスし、かつカバレッジが100%に達していなければならない

### Requirement: Static Type Checking
Mypyを使用して、型定義の不整合を検出しなければならない (SHALL)。

#### Scenario: Running type checks
- **WHEN** `mypy .` コマンドを実行する
- **THEN** 関数の引数や戻り値の型不整合が検出されてはならない

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