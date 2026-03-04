## Why

現在、ローカルでのデバッグ時に FastAPI アプリケーション (`uv run`) と ngrok を別々のターミナルで手動起動する必要があり、開発開始時の手間がかかっています。また、ngrok のドメインや認証トークンなどの設定が起動コマンドに依存しており、共有や管理が不便です。これを Docker Compose で統合することで、開発環境の構築を自動化し、チーム全体で一貫したデバッグ環境を迅速に立ち上げられるようにします。

## What Changes

- **Dockerfile の追加**: `uv` を使用した FastAPI アプリケーション用の Docker イメージを定義します。開発効率向上のため、ソースコードをボリュームマウントし、ホットリロードを有効にします。
- **docker-compose.yml の追加**: `app` (FastAPI) と `ngrok` (トンネル) の 2 つのサービスを定義します。ngrok は Docker ネットワーク経由で内部の `app:8000` を参照するように設定します。
- **環境変数管理の統合**: ngrok の認証トークン (`NGROK_AUTHTOKEN`) と静的ドメイン (`NGROK_DOMAIN`) を `.env` ファイルで管理できるようにし、`.env.example` にこれらの項目を追加します。
- **設定クラスの拡張**: `src/core/config.py` で ngrok 関連の設定を読み込めるようにし、必要に応じてアプリケーション内から参照可能にします。

## Capabilities

### New Capabilities
- `docker-development-environment`: Docker Compose を使用して、FastAPI と ngrok が連携した開発環境をコマンド一つで起動できる機能。

### Modified Capabilities
- (なし)

## Impact

- **開発ワークフロー**: `uv run` による直接起動に加え、`docker compose up` による起動が推奨されるようになります。
- **環境設定**: `.env` ファイルに ngrok 関連の設定（トークン、ドメイン）を追加する必要があります。
- **依存関係**: Docker および Docker Compose が開発環境の前提条件に追加されます。
