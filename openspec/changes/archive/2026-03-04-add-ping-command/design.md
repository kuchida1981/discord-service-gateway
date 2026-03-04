## Context

現在の実装は Discord からの PING (Type 1) に対する PONG 応答のみをサポートしています。Ed25519 による署名検証は `src/api/deps.py` で実装されており、FastAPI の依存注入を介して `src/api/routes.py` で利用されています。
`/ping` スラッシュコマンドを追加するには、この既存のフローを拡張し、アプリケーションコマンドを適切に処理・応答する仕組みが必要です。

## Goals / Non-Goals

**Goals:**
- `Interaction Type 2` (APPLICATION_COMMAND) を受信し、`data.name` に基づいて処理を振り分ける。
- `/ping` コマンドに対して `Pong!` と即時応答（Type 4）を返す。
- Discord API に対してコマンドを登録するためのスタンドアロンスクリプトを作成する。
- 開発時の即時反映のため、特定の Guild（サーバー）に対してコマンドを登録できるようにする。

**Non-Goals:**
- 高度なコマンドルーター（大規模なプラグインシステム等）の導入。今回は `routes.py` 内でのシンプルな分岐にとどめる。
- インタラクションの遅延応答（Type 5, `defer`）の実装。`/ping` は即時応答で十分なため。

## Decisions

### 1. Simple Command Dispatching in `routes.py`
- **Choice:** `if-elif` による分岐
- **Rationale:** 現時点ではコマンドが `/ping` 1つのみであり、複雑なルーターを導入するとオーバーヘッドが大きいため。将来的にコマンドが増えた段階で、`src/commands/` への切り出しを検討する。

### 2. Command Registration with `httpx`
- **Choice:** `httpx` を利用した Python スクリプト
- **Rationale:** プロジェクトですでに `httpx` が依存関係に含まれており、追加のライブラリ（discord.py 等）を導入せずに軽量に実装できるため。

### 3. Guild-Specific Registration for Development
- **Choice:** `DISCORD_GUILD_ID` を使用したギルドコマンド登録
- **Rationale:** グローバルコマンドは反映に最大1時間かかる場合があるが、ギルドコマンドは即座に反映されるため、開発効率を優先する。

## Risks / Trade-offs

- **[Risk] 環境変数の不足** → **[Mitigation]** `pydantic-settings` を使用している `src/core/config.py` に、`DISCORD_TOKEN` や `DISCORD_APPLICATION_ID` などの必須項目を追加し、起動時にバリデーションを行う。
- **[Risk] 署名検証エラー** → **[Mitigation]** `/ping` コマンドに対しても既存の `verify_discord_signature` 依存注入をそのまま適用し、一貫したセキュリティを担保する。
