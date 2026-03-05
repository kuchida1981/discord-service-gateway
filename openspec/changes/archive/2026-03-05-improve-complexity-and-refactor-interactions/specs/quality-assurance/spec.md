## MODIFIED Requirements

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
