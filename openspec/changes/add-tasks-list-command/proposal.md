## Why

Discord から Google Tasks のアクティブなタスク一覧を迅速に確認できるようにするため。既存の n8n ワークフロー資産を活用しつつ、外部 API の遅延による Discord の 3 秒ルール（レスポンスタイムアウト）を回避する堅牢な実装を目指します。

## What Changes

- **新しいスラッシュコマンド**: `/dsg tasks list` を追加し、現在のアクティブなタスクを一覧表示します。
- **非同期応答の導入**: Discord の `DEFERRED_CHANNEL_MESSAGE_WITH_SOURCE` (Type 5) を採用し、3 秒以上の処理時間を要する場合でも「考え中...」と表示してから結果を反映させます。
- **n8n 連携**: タスクの取得と整形を n8n ワークフローに委譲し、ゲートウェイは Webhook を介して結果を受け取ります。
- **UI/UX**: タスク名、期限、ステータスを Markdown 形式で読みやすく表示します。

## Capabilities

### New Capabilities
- `google-tasks-integration`: n8n を介して Google Tasks からタスク一覧を取得し、Discord に表示する機能。
- `discord-deferred-response`: 外部サービスの遅延に対応するため、Discord インタラクションを一度保留し、バックグラウンドで結果を更新する汎用的な基盤。

### Modified Capabilities
- `n8n-integration`: 既存のヘルスチェックに加え、具体的な業務ロジック（タスク取得）の呼び出しに対応するための拡張。

## Impact

- **API ハンドラ**: `src/api/handlers.py` に非同期タスク処理（FastAPI BackgroundTasks 等）を導入します。
- **サービス層**: `src/services/n8n.py` にタスク一覧取得用の新しい Webhook クライアントメソッドを追加します。
- **コマンド登録**: `src/cli/register_commands.py` および `src/api/models.py` に新しいコマンド定義を追加します。
- **設定**: `.env` に n8n の新しい Webhook URL (`N8N_TASKS_LIST_URL`) を追加します。
