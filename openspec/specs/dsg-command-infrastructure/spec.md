## Purpose

`/dsg` トップレベルコマンドを親として、サービス統合コマンドを階層的に管理するための基盤仕様。

## Requirements

### Requirement: DSG Command Namespace
システムは、すべてのサービス統合コマンドの親として `/dsg` トップレベルコマンドを提供しなければならない (SHALL)。

#### Scenario: User types /dsg
- **WHEN** ユーザーが Discord で `/dsg` を入力する
- **THEN** Discord UI 上でサブコマンドグループ（n8n 等）およびサブコマンドの選択肢が表示されなければならない

### Requirement: Hierarchical Interaction Parsing
システムは、受信したインタラクションの `options` 構造を階層的に解析し、ネストされたサブコマンドを正しく識別しなければならない (SHALL)。

#### Scenario: Subcommand resolution
- **WHEN** システムが `name: dsg` のインタラクションを受信し、`options` に `name: n8n`, `options` に `name: health` が含まれている
- **THEN** システムは n8n ヘルスチェック処理を実行しなければならない
