## Why

Cloud Run へのデプロイ時に `DISCORD_TOKEN` および `DISCORD_APPLICATION_ID` 環境変数が設定されていないため、アプリケーション起動時のコマンド登録処理で `RuntimeError` が発生し、正常に起動できない状態を解消するため。

## What Changes

- `.github/workflows/deploy.yml` の `gcloud run deploy` ステップに `DISCORD_TOKEN`, `DISCORD_APPLICATION_ID`, `DISCORD_GUILD_ID` を `--set-env-vars` 引数として追加。
- GitHub Secrets からこれらの値を読み込むように設定。

## Capabilities

### New Capabilities
<!-- None -->

### Modified Capabilities
- `ci-cd-pipeline`: デプロイプロセスにおいて、アプリケーション実行に必要な環境変数を正しく注入する要件を追加。

## Impact

- GitHub Actions の `Deploy to Cloud Run` ワークフロー
- Cloud Run サービスの環境変数設定
- アプリケーションの起動シーケンス（正常にコマンド登録が完了するようになる）
