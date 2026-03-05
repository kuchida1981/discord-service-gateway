## Why

`src/api/handlers.py` のコマンドルーティングが `dict.get()` と `isinstance` チェックのネストで実装されており、コマンドを追加するたびに深さが増す構造になっている。`/dsg <target> <action>` の体系でコマンドが今後増加する予定であり、今のうちに見通しのよい設計に改める。

## What Changes

- Discord のインタラクションデータ構造を表す Pydantic モデル群を新設する
- `routes.py` でシステム境界（`json.loads`）直後に Pydantic モデルへパースし、以降は型付きオブジェクトで扱う
- `handlers.py` の深いネストを廃止し、`Literal` 型と discriminated union による型ディスパッチへ置き換える
- 未知のコマンド名が届いた場合は HTTP 400 を返す（現在はサイレントに `{"message": "received"}` を返している）

## Capabilities

### New Capabilities

なし

### Modified Capabilities

- `slash-commands`: 未知のコマンド名に対するエラー応答要件を追加する

## Impact

- `src/api/handlers.py`: ルーティングロジック全面改修
- `src/api/routes.py`: Pydantic モデルへのパース追加
- 新規ファイル: `src/api/models.py`（Pydantic モデル定義）
- 既存テストの更新は必須。テストは厳しい水準で整備されており、実装変更に合わせてすべて通る状態を維持しなければならない