## Why
プルリクエスト（PR）の品質管理を自動化し、OpenSpecの運用ルール（Issueの紐付け、TODOの完遂、アーカイブの徹底）を確実に実行するためのガードレールを導入します。また、Draft PR状態では不要なチェックをスキップすることで、CIリソースの節約と開発体験の向上を図ります。

## What Changes
- `python-checks.yaml` に Draft PR 時のスキップロジックを追加。
- `check-openspec.yml` を新規作成し、OpenSpecの整合性とアーカイブ状況を検証。
- `check-pr-issue.yml` を新規作成し、PRとIssueの紐付けを検証。
- `check-todo.yml` を新規作成し、PR本文内のチェックリストが完了しているか検証（Draft PRでも実行）。

## Capabilities

### New Capabilities
- `qa-automation`: PR作成からマージまでの品質管理フローを自動化する能力。
- `openspec-compliance`: OpenSpecの設計原則および運用ルールへの準拠を自動検証する能力。

### Modified Capabilities
- `quality-assurance`: 既存の品質保証プロセスに、PRメタデータ（Issue, TODO）の検証とDraft制御の要件を追加。

## Impact
- `.github/workflows/` 内の既存ファイルの修正と新規ファイルの追加。
- GitHub Actions の実行フローが、PRの `draft` ステータスに応じて動的に変化するようになります。
