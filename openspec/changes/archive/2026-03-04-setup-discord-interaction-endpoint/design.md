## Context

DiscordのInteraction Endpointを新規に構築する。
DiscordはInteractionの送信先としてHTTPS POSTエンドポイントを要求し、そこではED25519アルゴリズムによるリクエストの署名検証が必須となる。
この署名検証を正しく行わなければ、Discord Developer Portalでのエンドポイント登録が完了できず、スラッシュコマンド等の機能を利用できない。

## Goals / Non-Goals

**Goals:**
- `uv` を用いた堅牢なPython開発環境の構築。
- FastAPIを使用した、署名検証機能付きの `/interactions` エンドポイントの実装。
- Discordからの PING リクエストに対する PONG レスポンスの実装。
- `ruff`, `pytest`, `mypy` による自動品質チェックの統合。

**Non-Goals:**
- スラッシュコマンドの実装（次フェーズ）。
- n8n API との具体的な連携処理（次フェーズ）。
- Google Cloud Run への実際のデプロイ（Dockerfile の作成までを本フェーズの視野とする）。

## Decisions

### 1. Package Management with `uv`
- **Choice:** `uv`
- **Rationale:** pipよりも圧倒的に高速であり、`pyproject.toml` による依存関係管理と仮想環境構築を透過的に行えるため。
- **Alternatives:** Poetry, pipenv. (いずれも速度面や設定の簡潔さでuvに劣る)

### 2. Signature Verification with `pynacl`
- **Choice:** `pynacl` (Python binding for libsodium)
- **Rationale:** Discord公式ドキュメントで推奨されているED25519署名検証ライブラリであり、信頼性が高い。
- **Implementation:** FastAPIの依存注入（Depends）またはミドルウェアとして実装し、リクエストの `X-Signature-Ed25519` と `X-Signature-Timestamp` を検証する。

### 3. Application Structure
```text
src/
├── main.py        # FastAPI アプリ初期化とライフサイクル管理
├── api/
│   ├── routes.py  # ルーティング定義
│   └── deps.py    # 署名検証などの依存注入用関数
└── core/
    └── config.py  # 環境変数 (DISCORD_PUBLIC_KEY等) の管理
```
- **Rationale:** 将来の拡張性を考え、ビジネスロジックとルーティングを分離しやすくするため。

### 4. Configuration Management
- **Choice:** `pydantic-settings`
- **Rationale:** 環境変数のバリデーション（必須項目のチェック等）を型安全に行えるため。

## Risks / Trade-offs

- **[Risk] Signature Verification Failure** → **[Mitigation]** Discord公式のテストケースやライブラリを活用し、正しい検証ロジックを担保する。また、ローカルでの疎通確認には `ngrok` を使用する。
- **[Risk] Secrets Leakage** → **[Mitigation]** `.env` を `.gitignore` に追加し、絶対にコミットされないようにする。
- **[Trade-off] Fast development vs Rigor** → **[Decision]** 初回から `ruff`, `mypy` を導入することで、長期的なメンテナンスコストを下げる。
