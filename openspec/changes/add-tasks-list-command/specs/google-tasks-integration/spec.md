## ADDED Requirements

### Requirement: Google Tasks List Display
システムは `/dsg tasks list` コマンドを受信した際、Google Tasks の現在アクティブなタスク一覧を表示しなければならない (SHALL)。

#### Scenario: Display active tasks
- **WHEN** ユーザーが `/dsg tasks list` を実行し、n8n からタスク一覧が正常に返された場合
- **THEN** システムはタスク名、期限、ステータスを含む Markdown 形式のメッセージを表示しなければならない

### Requirement: Google Tasks Empty State
システムは、アクティブなタスクが存在しない場合、その旨をユーザーに通知しなければならない (SHALL)。

#### Scenario: No active tasks
- **WHEN** ユーザーが `/dsg tasks list` を実行し、n8n から「タスクなし」のレスポンスが返された場合
- **THEN** システムは `現在アクティブなタスクはありません。` と表示しなければならない
