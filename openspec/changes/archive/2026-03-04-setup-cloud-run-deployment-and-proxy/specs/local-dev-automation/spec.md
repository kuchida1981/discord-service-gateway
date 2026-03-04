## ADDED Requirements

### Requirement: Docker Compose Lifecycle Hooks for Mode Toggling
システムは、`docker compose up` 起動時に Cloud Run を `dev` モードに切り替え、`docker compose down` 停止時に `prod` モードへ自動的に戻さなければならない (SHALL)。

#### Scenario: Auto-switch to dev mode on startup
- **WHEN** ユーザーが `dev.sh up`（または同等のラッパー）を実行し、ローカルコンテナを起動する
- **THEN** Cloud Run の `MODE` が `dev` に切り替わり、リクエストがローカルに転送されるようになる

#### Scenario: Auto-switch to prod mode on shutdown
- **WHEN** ユーザーが `dev.sh down`（または同等のラッパー）を実行し、ローカルコンテナを停止する
- **THEN** Cloud Run の `MODE` が `prod` に戻り、Cloud Run 自身のロジックが有効にならなければならない
