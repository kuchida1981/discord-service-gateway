## ADDED Requirements

### Requirement: Docker Build Check
変更によって Docker イメージのビルドが破損していないことを検証しなければならない (SHALL)。

#### Scenario: Verify Dockerfile build in CI
- **WHEN** CI ジョブが実行される
- **THEN** `docker build` コマンドが実行され、エラーなしで完了しなければならない
