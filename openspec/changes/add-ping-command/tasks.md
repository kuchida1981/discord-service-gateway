## 1. Configuration & Core

- [x] 1.1 `src/core/config.py` に `DISCORD_TOKEN`, `DISCORD_APPLICATION_ID`, `DISCORD_GUILD_ID` を追加する。
- [x] 1.2 `.env.example` に新しい環境変数のプレースホルダーを追加する。

## 2. Interaction Handling

- [x] 2.1 `src/api/routes.py` を修正し、`Interaction Type 2` (APPLICATION_COMMAND) の受信処理を追加する。
- [x] 2.2 `/ping` コマンドが受信された際に、`Pong!` というレスポンスを返すロジックを実装する。

## 3. Command Registration

- [x] 3.1 `scripts/register_commands.py` を新規作成し、`httpx` を使用して Discord API にコマンドを登録する機能を実装する。

## 4. Testing & Validation

- [x] 4.1 `tests/test_interactions.py` に `/ping` コマンドの正常系テストケースを追加する。
- [x] 4.2 `pytest` を実行し、すべてのテストがパスすることを確認する。
