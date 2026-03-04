## Purpose

Docker Compose を使用して、FastAPI アプリケーションと ngrok トンネルを単一コマンドで起動できる開発環境を提供するための仕様。

## Requirements

### Requirement: Docker Compose による統合開発環境の提供
システムは、`docker compose up` コマンド一つで、FastAPI アプリケーションと ngrok トンネルの両方を起動できなければならない（SHALL）。

#### Scenario: 開発環境の正常起動
- **WHEN** ユーザーがプロジェクトルートで `docker compose up -d` を実行する
- **THEN** `app` コンテナと `ngrok` コンテナが正常に起動し、互いに通信可能な状態になる

### Requirement: ソースコードのホットリロード
開発環境は、ホストマシン上のソースコード（`src/` ディレクトリ配下）の変更を検知し、コンテナ内の FastAPI アプリケーションを自動的に再起動しなければならない（SHALL）。

#### Scenario: コード変更の即時反映
- **WHEN** ユーザーがホスト側の `src/api/routes.py` を編集して保存する
- **THEN** `app` コンテナ内の uvicorn サーバーが変更を検知してリロードされ、新しいコードが適用される

### Requirement: ngrok による外部エンドポイントの提供
`ngrok` サービスは、指定された静的ドメインを使用して、内部の `app:8000` サービスを HTTPS 経由でインターネットに公開しなければならない（SHALL）。

#### Scenario: 外部からのアクセス
- **WHEN** `ngrok` コンテナが起動し、`NGROK_DOMAIN` に設定された URL に HTTPS リクエストを送信する
- **THEN** リクエストが `app` コンテナのポート 8000 に正しく転送され、有効なレスポンスが返される

### Requirement: 環境変数による設定管理
システムは、ngrok の認証トークンおよびドメイン情報を、ホストマシンの `.env` ファイルから読み込み、`ngrok` サービスの設定に反映しなければならない（SHALL）。

#### Scenario: 設定の動的反映
- **WHEN** `.env` ファイルに `NGROK_AUTHTOKEN` と `NGROK_DOMAIN` を記述して `docker compose up` を実行する
- **THEN** `ngrok` コンテナがそれらの値を使用してトンネルを確立する
