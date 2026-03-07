## Purpose

ローカル開発環境の起動・停止に伴う、外部サービス（Cloud Run）の状態変更を自動化し、シームレスな開発体験を提供することを目的とする。

## Requirements

### Requirement: Docker Compose Lifecycle Hooks for Mode Toggling
システムは、`docker compose up` 起動時に Cloud Run を `dev` モードに切り替え、`docker compose down` 停止時に `prod` モードへ自動的に戻さなければならない (SHALL)。

#### Scenario: Auto-switch to dev mode on startup
- **WHEN** ユーザーが `dev.sh up`（または同等のラッパー）を実行し、ローカルコンテナを起動する
- **THEN** Cloud Run の `MODE` が `dev` に切り替わり、リクエストがローカルに転送されるようになる

#### Scenario: Auto-switch to prod mode on shutdown
- **WHEN** ユーザーが `dev.sh down`（または同等のラッパー）を実行し、ローカルコンテナを停止する
- **THEN** Cloud Run の `MODE` が `prod` に戻り、Cloud Run 自身のロジックが有効にならなければならない

### Requirement: Sync Environment Variables to Cloud Run
システムは、`dev.sh up` 実行時にプロキシ動作（Cloud Run 転送）に必要な環境変数を、ローカルの `.env` から Cloud Run へ自動的に同期しなければならない (SHALL)。

#### Scenario: Auto-sync public key on startup
- **WHEN** ユーザーが `dev.sh up` を実行し、`DISCORD_PUBLIC_KEY` がローカルと Cloud Run で異なっている
- **THEN** システムは `gcloud` を介して Cloud Run の `DISCORD_PUBLIC_KEY` をローカルの値で更新する

### Requirement: Enforce Container Freshness on Startup
システムは、`dev.sh up` 実行時に、`.env` ファイルが変更されている場合に必ず Docker コンテナが再起動されることを保証しなければならない (SHALL)。

#### Scenario: Recreate container when .env changes
- **WHEN** ユーザーが `.env` を書き換えてから `dev.sh up` を実行する
- **THEN** Docker Compose は `.env` の変更を検知し、対象のサービスコンテナを再作成する

### Requirement: Validate Environment Variables against Example
システムは、`dev.sh up` 実行時に `.env` ファイルと `.env.example` を比較し、必要な変数が不足している場合にユーザーに警告しなければならない (SHALL)。

#### Scenario: Warn on missing variables
- **WHEN** `.env.example` にある変数が `.env` に存在しない状態で `dev.sh up` を実行する
- **THEN** システムは不足している変数名を標準出力に警告として表示する
