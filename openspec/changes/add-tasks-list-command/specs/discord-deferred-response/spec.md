## ADDED Requirements

### Requirement: Deferred Response Immediate Acknowledgment
システムは、時間のかかる処理が必要なコマンドを受信した際、Discord のタイムアウト（3秒）を回避するために即座に応答を返さなければならない (SHALL)。

#### Scenario: User triggers long-running command
- **WHEN** システムが `/dsg tasks list` 等の非同期処理が必要なインタラクションを受信する
- **THEN** システムは即座に `DEFERRED_CHANNEL_MESSAGE_WITH_SOURCE` (Type 5) を返さなければならない

### Requirement: Background Message Update
システムは、Deferred Response を返した後、バックグラウンドで処理を完了させ、元のメッセージを更新しなければならない (SHALL)。

#### Scenario: Successful background update
- **WHEN** システムがバックグラウンド処理を完了し、有効な `interaction_token` を保持している場合
- **THEN** システムは Discord の Webhook API (`PATCH /messages/@original`) を使用して、元のメッセージを最終的な結果で更新しなければならない
