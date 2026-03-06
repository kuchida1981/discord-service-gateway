## Context

現在のシステムは Discord のスラッシュコマンドに対して即時応答を返していますが、Google Tasks API や n8n ワークフローの呼び出しは、ネットワーク遅延や処理内容によって Discord の 3 秒タイムアウトを超えるリスクがあります。
本設計では、この問題を解決するために Discord の Deferred Response 機能を導入し、バックグラウンドでのメッセージ更新を可能にします。

## Goals / Non-Goals

**Goals:**
- Discord の 3 秒タイムアウトを確実に回避する非同期応答フローの実装。
- n8n Webhook と連携した Google Tasks 一覧取得機能の追加。
- `/dsg tasks list` コマンドの定義と登録。
- 他のコマンドでも再利用可能な非同期更新パターンの確立。

**Non-Goals:**
- Google Tasks API の直接呼び出し（n8n に委譲する）。
- タスクの追加・編集・削除機能（今回は一覧表示のみ）。
- 複雑なページネーションの実装。

## Decisions

### 1. 非同期処理に FastAPI の `BackgroundTasks` を採用
- **理由**: システムが FastAPI で構築されており、標準機能で軽量な非同期処理が可能であるため。Celery 等の外部ワーカーは現状の規模ではオーバーエンジニアリングと判断。
- **代替案**: `asyncio.create_task` (エラーハンドリングやライフサイクル管理が複雑になるため見送り)。

### 2. Discord Deferred Response (Type 5) の使用
- **理由**: ユーザーに「処理中」であることを明示しつつ、後からリッチな情報を届ける Discord 推奨のパターンであるため。
- **フロー**: ゲートウェイが `{"type": 5}` を返却 → バックグラウンドで n8n を実行 → `PATCH /webhooks/{id}/{token}/messages/@original` でメッセージを更新。

### 3. n8n からのレスポンス形式を Markdown テキストに固定
- **理由**: ゲートウェイ側のロジックを最小限に抑え、表示の微調整を n8n 側（ノーコード側）で完結させるため。
- **ワークフローの責任**: ユーザーは n8n 上で以下の仕様を満たすワークフローを構築する必要があります。
    - **Trigger**: Webhook (Method: POST)
    - **Logic**: Google Tasks API からタスクを取得し、読みやすい Markdown 文字列に変換。
    - **Response**: HTTP 200 OK と共に、整形済みのテキスト（`text/plain` または `application/json` の content フィールド）を返却。

### 4. インターフェース仕様（n8n ↔ Gateway）

**Request:**
- `POST {N8N_TASKS_LIST_URL}`
- Body: `{}` (現状、パラメータは不要)

**Expected Response (Markdown):**
```text
### 📝 Google Tasks 一覧
- [ ] タスク1 (期限: 2026-03-07)
- [ ] 期限なしのタスク
- [x] 完了済みのタスク (表示するかは n8n 側で制御)
```

## Risks / Trade-offs

- **[Risk] n8n 側での極端な遅延** → [Mitigation] バックグラウンドタスク内で 10 秒程度のタイムアウトを設定し、失敗時は「取得に失敗しました」というメッセージで更新する。
- **[Risk] interaction_token の有効期限** → [Mitigation] Discord のトークンは 15 分間有効であり、数秒〜数十秒の処理には十分。
- **[Trade-off] 実行の可視性** → バックグラウンド処理のエラーは Discord 上では「更新されない」か「エラーメッセージ」として現れるため、サーバーログへの適切な記録を徹底する。
