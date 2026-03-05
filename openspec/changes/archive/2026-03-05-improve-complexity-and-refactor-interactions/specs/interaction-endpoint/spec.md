## MODIFIED Requirements

### Requirement: Application Command Interaction Handling
システムは Discord からのアプリケーションコマンドインタラクション（Type 2: APPLICATION_COMMAND）を適切に受信し、コマンド名に基づいて処理を分岐させなければならない (SHALL)。
コマンドの具体的な処理ロジックは、専用のハンドラーモジュール（`src/api/handlers.py`）に委譲しなければならない。

#### Scenario: Handle application command interaction
- **WHEN** システムが `{"type": 2, "data": {"name": "ping", ...}}` を含む POST リクエストを受信する
- **THEN** システムは `data.name` を識別し、定義されたコマンドハンドラに処理を委譲しなければならない

#### Scenario: Handle unknown application command
- **WHEN** システムが認識できないコマンド名を含む APPLICATION_COMMAND を受信する
- **THEN** システムは `{"message": "received"}` を返さなければならない
