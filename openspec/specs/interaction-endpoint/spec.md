## Purpose

DiscordのInteraction Endpoint URLを検証し、署名検証を行って安全にInteractionを受け取るための仕様。

## Requirements

### Requirement: Discord Interaction Endpoint URL Verification
DiscordからのInteraction Endpoint URLの検証リクエスト（Type 1: PING）に正しく応答しなければならない (SHALL)。

#### Scenario: Handle PING interaction from Discord
- **WHEN** システムが `{"type": 1}` を含む POST リクエストを `/interactions` で受信する
- **THEN** システムは HTTP 200 OK と共に `{"type": 1}` (PONG) を返さなければならない

### Requirement: Interaction Signature Verification
すべての `/interactions` へのリクエストは、DiscordのPublic Keyを使用して署名検証を行わなければならない (SHALL)。

#### Scenario: Successful signature verification
- **WHEN** 有効な `X-Signature-Ed25519` と `X-Signature-Timestamp` を含むリクエストを受信する
- **THEN** システムはリクエストの署名を検証し、有効であればリクエストの `type` に基づいた適切な処理を継続しなければならない

### Requirement: Application Command Interaction Handling
システムは Discord からのアプリケーションコマンドインタラクション（Type 2: APPLICATION_COMMAND）を適切に受信し、コマンド名に基づいて処理を分岐させなければならない (SHALL)。

#### Scenario: Handle application command interaction
- **WHEN** システムが `{"type": 2, "data": {"name": "ping", ...}}` を含む POST リクエストを受信する
- **THEN** システムは `data.name` を識別し、定義されたコマンドハンドラに処理を委譲しなければならない

### Requirement: Health Check Endpoint
システムの生存確認のためのエンドポイントを提供しなければならない (SHALL)。

#### Scenario: Root endpoint response
- **WHEN** `GET /` にリクエストを送信する
- **THEN** システムは HTTP 200 OK と共にシステムのステータス（例：{"status": "ok"}）を返さなければならない
