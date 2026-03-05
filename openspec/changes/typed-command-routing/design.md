## Context

現在の `src/api/handlers.py` は Discord の `APPLICATION_COMMAND` インタラクションを処理するとき、`dict.get()` と `isinstance` チェックを5段ネストで記述している。`/dsg <target> <action>` のコマンド体系でコマンドが増加する予定であり、コマンドを1つ追加するたびにネストが深くなる。

`routes.py` でも `interaction.get("type")` を生の dict アクセスで行っており、システム境界でのパースが不完全な状態になっている。

既存テストは HTTP 統合テストとして充実しており、すべて通る状態を維持しなければならない。

## Goals / Non-Goals

**Goals:**
- Discord インタラクションデータを Pydantic モデルで型付けし、`isinstance` チェックを廃止する
- `Literal` 型と discriminated union によりルーティングを型レベルで表現する
- 未知のコマンドはエラーとして扱い、問題を隠さない
- システム境界（`json.loads` 直後）でのパースを `routes.py` に集約する
- 既存の統合テストをすべてパスし、新規ロジックにはユニットテストを追加する

**Non-Goals:**
- コマンドのふるまい自体の変更
- `/ping` 以外のトップレベルコマンドの追加
- Discord API との通信層の変更

## Decisions

### 決定1: `Literal` 型と discriminated union でコマンド構造を表現する

コマンド名を `name: str` ではなく `Literal` で定義し、Pydantic の discriminated union を活用する。

```
CommandData = Annotated[
    PingCommandData | DsgCommandData,
    Field(discriminator="name")
]

class PingCommandData(BaseModel):
    name: Literal["ping"]

class HealthOption(BaseModel):
    name: Literal["health"]
    type: int

class N8nGroup(BaseModel):
    name: Literal["n8n"]
    type: int
    options: list[HealthOption]

class DsgCommandData(BaseModel):
    name: Literal["dsg"]
    type: int
    options: list[N8nGroup]  # target が増えたら union に追加
```

パース時点でコマンド名が検証されるため、ルーティングは型の照合だけになる。

**採用しなかった選択肢**:
- `name: str` + ルックアップテーブル → 名前の検証とルーティングが別の仕組みになる。Literal の方が型と意味が一致している

### 決定2: 未知のコマンドは `ValidationError` としてエラー応答する

未知のコマンドが届いた場合、`register_commands` が正しく実行されていないことを意味する。サイレントに `{"message": "received"}` を返すのは問題を隠す。

`routes.py` で `ValidationError` をキャッチし、HTTP 400 を返す。

**現在の `{"message": "received"}` との違い**: 未知の *インタラクションタイプ*（将来 Discord が追加する可能性がある）は引き続き `{"message": "received"}` で受け流す。未知の *コマンド名* のみをエラーとする。

### 決定3: Pydantic モデルを `src/api/models.py` に新設する

`routes.py` と `handlers.py` の両方が参照するため独立したモジュールに置く。純粋なデータ定義のみを持ち、ビジネスロジックを含まない。

### 決定4: パースは `routes.py` のシステム境界で行う

`json.loads` の直後で `Interaction.model_validate()` を呼ぶ。以降のコードは型付きオブジェクトで扱える。`handlers.py` には `CommandData` 型の値が渡る。

### 決定5: テストにユニットテストを追加する

既存テストは HTTP 統合テストのみ。`models.py` のパース挙動（正常系・異常系）と `handlers.py` のルーティングはユニットテストで独立して検証する。これにより、コマンド追加時のテストが書きやすくなる。

## Risks / Trade-offs

- **コマンド追加時の変更箇所が増える**: Literal 方式では新コマンドごとに新モデルクラスと union への追加が必要。ただしその分、型チェックと意味が一致するため、追加漏れをコンパイル時に検出しやすい
- **Pydantic v2 の再帰モデル**: 自己参照モデルは `model_rebuild()` が必要な場合がある。実装時に確認する
- **`ValidationError` の HTTP 400 化**: Discord 側が 400 を受け取った場合の挙動を事前に確認しておく

## Migration Plan

1. `src/api/models.py` を新設（Pydantic モデル + Literal 定義）
2. `src/api/handlers.py` を改修（discriminated union による型ディスパッチ）
3. `src/api/routes.py` を改修（`model_validate` でパース、`ValidationError` → HTTP 400）
4. `tests/test_interactions.py` に `models.py` と `handlers.py` のユニットテストを追加
5. 既存の統合テストがすべてパスすることを確認

ロールバックが必要な場合は git revert で即時復旧可能。外部 API インターフェースは変わらない。