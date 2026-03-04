## ADDED Requirements

### Requirement: Ping Command Response
システムはスラッシュコマンド `/ping` を受信した際、即座にメッセージ `Pong!` を返さなければならない (SHALL)。

#### Scenario: User sends /ping
- **WHEN** システムが `data.name` が `ping` である `type: 2` インタラクションを受信する
- **THEN** システムは HTTP 200 OK と共に `{"type": 4, "data": {"content": "Pong!"}}` を返さなければならない

### Requirement: Discord Command Registration
システムは、定義されたスラッシュコマンドを Discord API に対して登録するための独立した手段を提供しなければならない (SHALL)。

#### Scenario: Register commands to a guild
- **WHEN** 開発者が登録スクリプトを実行し、`DISCORD_GUILD_ID` が設定されている
- **THEN** スクリプトは指定されたギルドに対してのみコマンドを登録する API リクエストを送信し、成功メッセージを表示しなければならない
