## ADDED Requirements

### Requirement: Unknown Command Rejection
システムは、登録されていないコマンド名を含む `APPLICATION_COMMAND` インタラクションを受信した場合、HTTP 400 を返さなければならない (SHALL)。未知のコマンドが届くことは `register_commands` が正しく実行されていないことを意味するため、サイレントに無視してはならない。

#### Scenario: Unregistered command name
- **WHEN** システムが `type: 2` のインタラクションを受信し、`data.name` が登録済みコマンド名（`ping`, `dsg`）のいずれにも一致しない
- **THEN** システムは HTTP 400 を返さなければならない
