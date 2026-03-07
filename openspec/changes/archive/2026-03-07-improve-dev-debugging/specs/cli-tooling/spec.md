## MODIFIED Requirements

### Requirement: Toggle development mode
システムは、`uv run toggle-mode` を通じて Cloud Run の動作モードを切り替え、必要に応じて関連する環境変数を同期しなければならない (SHALL)。

#### Scenario: Switch to dev mode with sync
- **WHEN** ユーザーが `uv run toggle-mode dev --url <url> --sync` を実行する
- **THEN** Cloud Run の `MODE` が `dev` になり、`FORWARD_URL` が設定され、かつ `SYNC_ENV_VARS` に定義された他の変数が同期される

#### Scenario: Switch to prod mode
- **WHEN** ユーザーが `uv run toggle-mode prod` を実行する
- **THEN** Cloud Run の `MODE` が `prod` に戻り、`FORWARD_URL` が削除される

## ADDED Requirements

### Requirement: Display Development Environment Status
システムは、現在のローカル開発環境と Cloud Run の接続状況、および環境変数の同期状況を一覧表示するコマンドを提供しなければならない (SHALL)。

#### Scenario: Check status
- **WHEN** ユーザーが `dev.sh status` を実行する
- **THEN** システムは現在の ngrok URL、Cloud Run モード、および `SYNC_ENV_VARS` の一致状況を表示する
