## 1. Pydantic モデルの新設

- [ ] 1.1 `src/api/models.py` を作成し、`CommandOption`（再帰）・`HealthOption`・`N8nGroup`・`PingCommandData`・`DsgCommandData`・`CommandData`（discriminated union）・`ApplicationCommandData`・`Interaction` を定義する
- [ ] 1.2 Pydantic v2 で再帰モデルが正しく解決されることを確認する（必要なら `model_rebuild()` を追加する）

## 2. routes.py の改修

- [ ] 2.1 `json.loads` 直後に `Interaction.model_validate()` を呼び、型付きオブジェクトで以降を処理するよう変更する
- [ ] 2.2 `ValidationError` をキャッチして HTTP 400 を返す処理を追加する
- [ ] 2.3 `interaction.get("type")` の生 dict アクセスを `interaction.type` の属性アクセスへ置き換える

## 3. handlers.py の改修

- [ ] 3.1 `handle_application_command` の引数を `dict[str, object]` から `CommandData` へ変更する
- [ ] 3.2 `isinstance` チェックとネストした `if` を discriminated union による型ディスパッチへ置き換える
- [ ] 3.3 `handle_dsg_command` を切り出し、`DsgCommandData` を受け取って target/action を属性アクセスで取得するよう実装する

## 4. テストの更新・追加

- [ ] 4.1 `models.py` のユニットテストを追加する（正常パース・不正なコマンド名・オプション欠損など）
- [ ] 4.2 未知のコマンド名が HTTP 400 を返すことを検証する統合テストを追加する（`test_interactions_unknown_command_returns_received` を HTTP 400 に更新する）
- [ ] 4.3 既存の統合テストがすべてパスすることを確認する
