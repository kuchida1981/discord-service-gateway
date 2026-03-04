## MODIFIED Requirements

### Requirement: Interaction Signature Verification
すべての `/interactions` へのリクエストは、DiscordのPublic Keyを使用して署名検証を行わなければならない (SHALL)。

#### Scenario: Successful signature verification
- **WHEN** 有効な `X-Signature-Ed25519` と `X-Signature-Timestamp` を含むリクエストを受信する
- **THEN** システムはリクエストの署名を検証し、有効であればリクエストの `type` に基づいた適切な処理を継続しなければならない

## ADDED Requirements

### Requirement: Application Command Interaction Handling
システムは Discord からのアプリケーションコマンドインタラクション（Type 2: APPLICATION_COMMAND）を適切に受信し、コマンド名に基づいて処理を分岐させなければならない (SHALL)。

#### Scenario: Handle application command interaction
- **WHEN** システムが `{"type": 2, "data": {"name": "ping", ...}}` を含む POST リクエストを受信する
- **THEN** システムは `data.name` を識別し、定義されたコマンドハンドラに処理を委譲しなければならない
