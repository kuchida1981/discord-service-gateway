## Purpose

プロジェクトのコード品質、堅牢性、および挙動を確実に担保するための静的解析とテストの仕様を定義する。
本仕様は、Ruffによる高速なLintとフォーマット、Pytestによる包括的な自動テスト、およびMypyによる静的型チェックを組み合わせ、
開発サイクル全体を通じて一貫した品質基準を維持することを目的としている。

## Requirements

### Requirement: Static Code Analysis and Formatting
Ruffを使用して、コードの静的解析とフォーマットの一貫性を保たなければならない (SHALL)。

#### Scenario: Running lint checks
- **WHEN** `ruff check .` コマンドを実行する
- **THEN** 未使用のインポートや構文ミスが検出されなければならない

#### Scenario: Running format checks
- **WHEN** `ruff format --check .` コマンドを実行する
- **THEN** コードのフォーマットがプロジェクトの規定（.ruff.toml）に適合していることを確認しなければならない

### Requirement: Automated Testing
Pytestを使用して、APIエンドポイントの動作が期待通りであることを検証しなければならない (SHALL)。

#### Scenario: Run API unit tests
- **WHEN** `pytest` コマンドを実行する
- **THEN** すべてのエンドポイント（`/`, `/interactions`）に対するテストケースがパスしなければならない

### Requirement: Static Type Checking
Mypyを使用して、型定義の不整合を検出しなければならない (SHALL)。

#### Scenario: Running type checks
- **WHEN** `mypy .` コマンドを実行する
- **THEN** 関数の引数や戻り値の型不整合が検出されなければならない
