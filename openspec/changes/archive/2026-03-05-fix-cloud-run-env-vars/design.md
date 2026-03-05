## Context

Cloud Run サービス `discord-gateway` は起動時に Discord のスラッシュコマンドを登録しようとしますが、その際に `DISCORD_TOKEN` などの環境変数が必要です。現在の GitHub Actions ワークフローではこれらの環境変数が `gcloud run deploy` 時に渡されておらず、デフォルト値の `"dummy_token"` が使用されて `RuntimeError` が発生しています。

## Goals / Non-Goals

**Goals:**
- `gcloud run deploy` コマンドを修正し、必要な環境変数をすべて注入する。
- GitHub Secrets を利用して、セキュアに環境変数を管理する。

**Non-Goals:**
- 今回の変更では Secret Manager への完全な移行（`--set-secrets`）は行わず、既存の `--set-env-vars` 方式を拡張するに留める（スピード重視）。

## Decisions

- **Decision 1: `--set-env-vars` の拡張**
  - **Rationale**: 既存のワークフローが既に `--set-env-vars` を使用しており、最小限の修正で済むため。
  - **Alternatives**: Google Cloud Secret Manager の使用（`--set-secrets`）。よりセキュアだが、GCP 側の IAM 権限設定やシークレットの作成が必要なため、今回は見送る。

- **Decision 2: 必要な環境変数のリストアップ**
  - 追加する変数: `DISCORD_TOKEN`, `DISCORD_APPLICATION_ID`, `DISCORD_GUILD_ID`
  - 既存の変数: `MODE`, `DISCORD_PUBLIC_KEY`

## Risks / Trade-offs

- **[Risk] GitHub Secrets の未設定** → [Mitigation] ワークフローのドキュメントまたはコメントに、必要なシークレット名を明記する。
- **[Trade-off] 平文環境変数の露出** → `--set-env-vars` は GCP コンソール上で値が見えてしまうが、開発初期段階としては許容範囲とする。
