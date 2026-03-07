## ADDED Requirements

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
