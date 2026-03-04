## Context

現在、FastAPI アプリケーションと ngrok トンネルを個別に手動起動しており、開発の開始に手間がかかっています。本デザインでは、Docker Compose を導入することで、これらを単一のコマンドで再現可能な環境として構築します。また、`uv` をベースとしたコンテナ構成により、高速なビルドと開発時のホットリロードを両立させます。

## Goals / Non-Goals

**Goals:**
- `docker compose up` による FastAPI と ngrok の一括起動の実現。
- ホスト上のソースコード変更をコンテナ内に即時反映（ホットリロード）させる。
- ngrok の認証トークンと静的ドメインを `.env` で一元管理し、コマンドライン引数への依存を排除する。
- `pydantic-settings` を通じて、アプリケーション内からも ngrok 関連の設定を参照可能にする。

**Non-Goals:**
- 本番環境用の Docker イメージの最適化（本件は開発環境に特化）。
- CI/CD パイプラインでの Docker 使用（将来的な課題とする）。
- DB やキャッシュなどのミドルウェアの追加（現時点では不要）。

## Decisions

### 1. ベースイメージの選択
- **Decision**: `ghcr.io/astral-sh/uv:python3.11-bookworm-slim` を使用する。
- **Rationale**: プロジェクトですでに `uv` を使用しており、依存関係の解決が非常に高速であるため。また、公式の `uv` イメージを使うことで Dockerfile の記述を簡素化できる。

### 2. ソースコードの同期方法
- **Decision**: Docker Volume を使用してホストのルートディレクトリをコンテナ内の `/app` にマウントする。
- **Rationale**: 開発中に `src/` 配下のファイルを編集した際、コンテナを再ビルドすることなく `uvicorn --reload` によるホットリロードを効かせるため。

### 3. ngrok の構成
- **Decision**: `ngrok/ngrok:latest` 公式イメージを使用し、`docker-compose.yml` の `command` フィールドで設定を注入する。
- **Rationale**: 独自イメージを作成する必要がなく、設定の変更（ドメインの変更など）が `docker-compose.yml` または `.env` の変更だけで完結するため。

### 4. 環境変数の管理
- **Decision**: `NGROK_AUTHTOKEN` と `NGROK_DOMAIN` を `.env` に定義し、`docker-compose.yml` の `environment` セクションでコンテナへ渡す。
- **Rationale**: セキュリティ上の理由からトークンをコードベースに含めないようにしつつ、開発者ごとに異なるドメインを使用できるようにするため。

## Risks / Trade-offs

- **[Risk] ngrok 認証トークンの未設定** → [Mitigation] `.env.example` に必須項目として明記し、設定されていない場合に ngrok コンテナのログでエラーが確認できるようにする。
- **[Trade-off] コンテナによるオーバーヘッド** → ネイティブでの実行（`uv run`）と比較して若干のオーバーヘッドがあるが、環境の一貫性と起動の簡便性が上回ると判断。引き続きネイティブ実行も可能な構成を維持する。
- **[Risk] ファイルパーミッションの差異 (macOS/Linux)** → [Mitigation] `uv` を非ルートユーザーで実行する設定を検討したが、開発環境の簡便性を優先し、デフォルト設定で運用を開始する。問題が発生した場合は `chown` 等の対策を講じる。

## Migration Plan

1. `.env.example` に ngrok 関連の変数を追加する。
2. `Dockerfile` を作成する。
3. `docker-compose.yml` を作成する。
4. `src/core/config.py` に設定項目を追加する。
5. README.md に Docker での起動方法を追記する（オプション）。
