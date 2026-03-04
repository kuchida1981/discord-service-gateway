## Why

Discordからのスラッシュコマンドを受け取り、n8nや他のWebサービスをコントロールするための堅牢なAPI基盤を構築する。
最初のステップとして、セキュリティ（署名検証）を担保しつつ、Discord Developer Portalとの疎通を確立する最小限のサーバーを構築し、開発サイクル（uv, ruff, pytest, ngrok）を整える。

## What Changes

- **Project Scaffolding**: `uv` によるパッケージ管理と、`ruff`, `pytest`, `mypy` による品質管理環境の構築。
- **FastAPI Base Implementation**:
    - 健康診断用の `GET /` エンドポイント。
    - Discord Interaction用の `POST /interactions` エンドポイント。
- **Security & Validation**:
    - `pynacl` を使用した ED25519 署名検証ロジックの実装。
    - Discordからの `PING` (Type 1) リクエストに対する `PONG` レスポンスの実装。
- **Local Debugging**: `ngrok` を活用したローカル開発・検証フローの確立。

## Capabilities

### New Capabilities
- `interaction-endpoint`: DiscordからのInteraction（特にType 1: PING）を受け取り、正しく署名検証を行ってレスポンスを返す能力。
- `quality-assurance`: `ruff`, `pytest`, `mypy` を使用して、コードの品質と堅牢性を自動的にチェックする能力。

### Modified Capabilities
- (なし: 新規プロジェクトのため)

## Impact

- `kuchida1981/discord-service-gateway` リポジトリの初期構造。
- Discord Developer Portal での "Interactions Endpoint URL" 設定が可能になる。
