## Purpose

開発・運用ツール（Discord コマンド登録、Cloud Run モード切替）を `uv run <command>` で実行できる標準化された CLI エントリポイントを提供し、`src/` パッケージと同等のコード品質基準を適用するための仕様。

## Requirements

### Requirement: CLI Tool Access via uv
システムは、`uv run <command>` を介してプロジェクトの管理ツールを実行できるエントリポイントを提供しなければならない (SHALL)。

#### Scenario: Register Discord commands
- **WHEN** ユーザーが `uv run register-commands` を実行する
- **THEN** `src/cli/register_commands.py` が実行され、Discord スラッシュコマンドが登録される

#### Scenario: Toggle development mode
- **WHEN** ユーザーが `uv run toggle-mode dev --url <url>` を実行する
- **THEN** `src/cli/toggle_mode.py` が実行され、Cloud Run の環境変数が更新される

#### Scenario: Switch to dev mode with sync
- **WHEN** ユーザーが `uv run toggle-mode dev --url <url> --sync` を実行する
- **THEN** Cloud Run の `MODE` が `dev` になり、`FORWARD_URL` が設定され、かつ `SYNC_ENV_VARS` に定義された他の変数が同期される

#### Scenario: Switch to prod mode
- **WHEN** ユーザーが `uv run toggle-mode prod` を実行する
- **THEN** Cloud Run の `MODE` が `prod` に戻り、`FORWARD_URL` が削除される

### Requirement: Display Development Environment Status
システムは、現在のローカル開発環境と Cloud Run の接続状況、および環境変数の同期状況を一覧表示するコマンドを提供しなければならない (SHALL)。

#### Scenario: Check status
- **WHEN** ユーザーが `dev.sh status` を実行する
- **THEN** システムは現在の ngrok URL、Cloud Run モード、および `SYNC_ENV_VARS` の一致状況を表示する

### Requirement: Integrated Quality Control for Tools
全ての CLI ツールは、アプリケーション本体と同じ Lint および型チェックのルール（Ruff, Mypy）を遵守しなければならない (SHALL)。

#### Scenario: Run linting on CLI tools
- **WHEN** ユーザーが `ruff check .` を実行する
- **THEN** `src/cli/` 配下のファイルもスキャン対象となり、ルール違反が報告される

#### Scenario: Run type check on CLI tools
- **WHEN** ユーザーが `mypy .` を実行する
- **THEN** `src/cli/` 配下のファイルも型チェックの対象となり、エラーが報告される
