## Purpose

Cloud Run 上で動作するプロキシ機能の要件を定義し、開発時のリクエスト転送や認証制御の挙動を確立する。

## Requirements

### Requirement: Cloud Run Interaction Proxying
Cloud Run 環境で実行されているシステムは、設定された `MODE` が `dev` の場合、受信した Interaction リクエストを署名検証後に指定された `FORWARD_URL` へ転送しなければならない (SHALL)。

#### Scenario: Forward interaction in dev mode
- **WHEN** システムが `MODE=dev` で動作しており、署名検証済みの有効な Interaction リクエストを受信する
- **THEN** システムはリクエストボディとヘッダーを保持したまま `FORWARD_URL` へ POST リクエストを送信し、そのレスポンスをクライアントに返さなければならない

### Requirement: Signature Verification Skipping in Local Mode
システムは、設定された `MODE` が `local` の場合、Discord からの署名検証をスキップし、リクエストを常に信頼済みとして処理しなければならない (SHALL)。

#### Scenario: Skip verification in local mode
- **WHEN** システムが `MODE=local` で動作しており、リクエストを受信する
- **THEN** システムは `X-Signature-Ed25519` ヘッダー等の検証を行わず、リクエストの処理を継続しなければならない

### Requirement: Mode Toggle Automation
システムは、外部スクリプトを介して Cloud Run の環境変数を更新し、`MODE`（`prod`/`dev`）および `FORWARD_URL` を即座に（数十秒以内に）変更できなければならない (SHALL)。

#### Scenario: Toggle to dev mode
- **WHEN** ユーザーが `scripts/toggle_mode.py dev --url <url>` を実行する
- **THEN** 指定された Cloud Run サービスの環境変数が更新され、新しいリビジョンがデプロイされる
