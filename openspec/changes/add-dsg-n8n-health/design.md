## Context

現在の Discord Service Gateway は `ping` コマンドのみを持つ単純な構造です。今後、n8n や GCP といった複数のサービスを統合していくにあたり、コマンドがフラットに並ぶと管理が困難になります。
Discord のサブコマンドグループ機能を利用して、`/dsg <service> <action>` という形式の階層構造を導入します。

## Goals / Non-Goals

**Goals:**
- `/dsg` トップレベルコマンドの実装と Discord への登録。
- サブコマンドグループ `n8n` とサブコマンド `health` の実装。
- インタラクション受信時に階層的なオプションを適切にパースし、処理を振り分けるロジックの実装。
- n8n のヘルスチェックエンドポイントへの外部通信の実装。

**Non-Goals:**
- 既存の `ping` コマンドの完全な削除（互換性のために当面維持するか、`/dsg` 配下へ追加するのみに留める）。
- n8n 以外のサービスの本格的な実装（今回の変更は基盤と n8n health のみにフォーカスする）。
- 詳細な権限管理システム（Discord 側の設定に依存する）。

## Decisions

### 1. コマンド構造の定義
Discord API の `CHAT_INPUT` コマンドにおいて、`type: 2` (SUB_COMMAND_GROUP) と `type: 1` (SUB_COMMAND) を使用します。
- `name: dsg` (Command)
  - `options`:
    - `name: n8n` (SUB_COMMAND_GROUP)
      - `options`:
        - `name: health` (SUB_COMMAND)

**理由:** Discord 標準の階層化手法であり、ユーザーインターフェース上も整理されて表示されるため。

### 2. インタラクション・パース・ロジック
`src/api/routes.py` において、`data["options"]` を再帰的、あるいは階層を追ってパースし、実行すべき関数を特定します。

**実装イメージ:**
```python
options = data.get("options", [])
if not options:
    return # handle top-level if any
group = options[0]
if group["name"] == "n8n":
    sub_options = group.get("options", [])
    sub_cmd = sub_options[0]
    if sub_cmd["name"] == "health":
        return await handle_n8n_health()
```

### 3. n8n 連携サービス
`src/services/n8n.py` を新設し、`httpx` を使用して `https://n8n.u-rei.com/healthz` にリクエストを送る責務を持たせます。

**理由:** API ルート (`routes.py`) に外部通信のロジックを直接書かず、サービス層として分離することでテストを容易にし、コードの再利用性を高めるため。

### 4. 設定の管理
`src/core/config.py` に `N8N_HEALTH_URL` を追加します。

## Risks / Trade-offs

- **[Risk] インタラクションのタイムアウト** → Discord は 3 秒以内にレスポンスを返す必要があります。n8n の応答が遅い場合、タイムアウトエラーになる可能性があります。
- **[Mitigation]** 適切なタイムアウト設定（例: 2.5秒）を `httpx` に設定し、遅延時には「一時的なエラー」をユーザーに返せるようにします。将来的に重い処理が必要になった場合は、`DEFERRED_CHANNEL_MESSAGE_WITH_SOURCE` を検討します。

- **[Trade-off] 単一コマンドから階層コマンドへの移行** → ユーザーが入力する手数が増える可能性があります。
- **[Decision]** しかし、機能が増えた際の管理性を優先し、早い段階で階層化を導入します。
