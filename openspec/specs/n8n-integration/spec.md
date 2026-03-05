## Purpose

n8n ワークフロー自動化サービスとの連携機能を提供する。第一段階として、n8n インスタンスの稼働状態を確認するヘルスチェック機能を実装し、Discord コマンド経由で状態を確認できるようにする。

## Requirements

### Requirement: n8n Health Check Execution
システムは、`/dsg n8n health` コマンドを受けた際、設定された n8n ヘルスチェックエンドポイントに対して HTTP GET リクエストを送信し、その結果を取得しなければならない (SHALL)。

#### Scenario: Request to n8n healthz
- **WHEN** ユーザーが `/dsg n8n health` コマンドを実行する
- **THEN** システムは `https://n8n.u-rei.com/healthz` (設定値) に対して 3 秒以内のタイムアウトで GET リクエストを送信しなければならない

### Requirement: n8n Status Response Message
システムは、n8n ヘルスチェックの結果に基づいて、ユーザーに成功または失敗のメッセージを返さなければならない (SHALL)。

#### Scenario: Successful n8n health check
- **WHEN** n8n から `{"status": "ok"}` というレスポンスを受信する
- **THEN** システムは `n8n status: ok ✅` というメッセージをユーザーに返さなければならない

#### Scenario: n8n health check failure
- **WHEN** n8n から 200 以外のステータスコード、または不正な JSON を受信する
- **THEN** システムは `n8n status: error ❌` というメッセージと共にエラー内容をユーザーに返さなければならない
