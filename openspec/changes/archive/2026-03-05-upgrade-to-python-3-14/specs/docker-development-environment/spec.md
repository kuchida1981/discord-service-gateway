## MODIFIED Requirements

### Requirement: Docker Compose による統合開発環境の提供
システムは、`docker compose up` コマンド一つで、FastAPI アプリケーションと ngrok トンネルの両方を起動できなければならない（SHALL）。アプリケーションは Python 3.14 環境で動作しなければならない。

#### Scenario: 開発環境の正常起動
- **WHEN** ユーザーがプロジェクトルートで `docker compose up -d` を実行する
- **THEN** `app` コンテナが Python 3.14 ベースで起動し、`ngrok` コンテナと共に正常に通信可能な状態になる
