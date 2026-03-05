## MODIFIED Requirements

### Requirement: Discord Command Registration
システムは、定義されたスラッシュコマンド（階層構造を含む）を Discord API に対して登録するための独立した手段を提供しなければならない (SHALL)。

#### Scenario: Register nested commands
- **WHEN** 開発者が登録スクリプトを実行し、`/dsg` 等のネストされた構造を持つコマンドが定義されている
- **THEN** スクリプトはそれらの構造を Discord の `SUB_COMMAND_GROUP` および `SUB_COMMAND` 型として正しく登録しなければならない

#### Scenario: Register commands to a guild
- **WHEN** 開発者が登録スクリプトを実行し、`DISCORD_GUILD_ID` が設定されている
- **THEN** スクリプトは指定されたギルドに対してのみコマンドを登録する API リクエストを送信し、成功メッセージを表示しなければならない
