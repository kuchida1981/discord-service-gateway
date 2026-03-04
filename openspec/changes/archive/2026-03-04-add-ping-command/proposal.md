## Why

現在、システムは Discord からの PING/PONG（接続確認）のみをサポートしており、実際のアプリケーションコマンド（スラッシュコマンド）を処理する機能がありません。動作確認および将来的な機能拡張の基礎として、最もシンプルなスラッシュコマンド `/ping` を実装する必要があります。

## What Changes

- `/interactions` エンドポイントにおいて、`Interaction Type 2` (APPLICATION_COMMAND) のハンドリングを追加します。
- スラッシュコマンド `/ping` に対して、`Pong!` と応答する機能を実装します。
- Discord API に対してコマンドを登録するためのユーティリティスクリプトを追加します。
- `/ping` コマンドの動作を検証するための自動テストを追加します。

## Capabilities

### New Capabilities
- `slash-commands`: スラッシュコマンドの基礎的なハンドリングと、Discord API へのコマンド登録機能。

### Modified Capabilities
- `interaction-endpoint`: PING/PONG 以外のインタラクション（APPLICATION_COMMAND）を処理できるように要件を拡張します。

## Impact

- `src/api/routes.py`: インタラクションタイプの分岐処理の追加。
- `tests/test_interactions.py`: スラッシュコマンド用のテストケースの追加。
- `scripts/register_commands.py` (新規): コマンド登録用ユーティリティ。
- `src/core/config.py`: コマンド登録に必要な環境変数（APP_ID, BOT_TOKEN 等）の管理。
