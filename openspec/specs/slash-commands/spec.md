## Purpose

Discord のスラッシュコマンド（APPLICATION_COMMAND）を定義し、適切に応答・登録するための仕様。

## Requirements

### Requirement: Ping Command Response
システムはスラッシュコマンド `/ping` を受信した際、即座にメッセージ `Pong!` を返さなければならない (SHALL)。

#### Scenario: User sends /ping
- **WHEN** システムが `data.name` が `ping` である `type: 2` インタラクションを受信する
- **THEN** システムは HTTP 200 OK と共に `{"type": 4, "data": {"content": "Pong!"}}` を返さなければならない

### Requirement: Discord Command Registration
システムは、定義されたスラッシュコマンド（階層構造を含む）を Discord API に対して登録するための独立した手段を提供しなければならない (SHALL)。

#### Scenario: Register nested commands
- **WHEN** 開発者が登録スクリプトを実行し、`/dsg` 等のネストされた構造を持つコマンドが定義されている
- **THEN** スクリプトはそれらの構造を Discord の `SUB_COMMAND_GROUP` および `SUB_COMMAND` 型として正しく登録しなければならない

#### Scenario: Register commands to a guild
- **WHEN** 開発者が登録スクリプトを実行し、`DISCORD_GUILD_ID` が設定されている
- **THEN** スクリプトは指定されたギルドに対してのみコマンドを登録する API リクエストを送信し、成功メッセージを表示しなければならない

### Requirement: Unknown Command Rejection
システムは、登録されていないコマンド名を含む `APPLICATION_COMMAND` インタラクションを受信した場合、HTTP 400 を返さなければならない (SHALL)。未知のコマンドが届くことは `register_commands` が正しく実行されていないことを意味するため、サイレントに無視してはならない。

#### Scenario: Unregistered command name
- **WHEN** システムが `type: 2` のインタラクションを受信し、`data.name` が登録済みコマンド名（`ping`, `dsg`）のいずれにも一致しない
- **THEN** システムは HTTP 400 を返さなければならない
