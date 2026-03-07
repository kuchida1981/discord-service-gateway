## ADDED Requirements

### Requirement: n8n Task List Webhook Execution
システムはタスク一覧の取得要求を受けた際、n8n で構成された特定の Webhook エンドポイントを呼び出さなければならない (SHALL)。

#### Scenario: Request to tasks list webhook
- **WHEN** システムが Google Tasks 一覧の取得を開始する
- **THEN** システムは環境変数 `N8N_TASKS_LIST_URL` で定義された URL に対して HTTP POST リクエストを送信しなければならない

### Requirement: n8n Task List Response Handling
システムは n8n から返されたレスポンスを、そのまま（または最小限の加工で）Discord のメッセージコンテンツとして採用しなければならない (SHALL)。

#### Scenario: Receive formatted tasks from n8n
- **WHEN** n8n Webhook がステータス 200 と共に Markdown 形式のテキストを返す
- **THEN** システムはそのテキストを Discord メッセージの `content` フィールドに設定しなければならない
