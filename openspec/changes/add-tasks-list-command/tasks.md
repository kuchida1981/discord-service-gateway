## 0. 事前準備 (ユーザー作業)

- [ ] 0.1 n8n 上で Webhook (POST) トリガーのワークフローを作成
- [ ] 0.2 Google Tasks API を呼び出し、アクティブなタスクを Markdown 文字列に整形して返すように構成
- [ ] 0.3 Webhook の公開 URL を取得し、ゲートウェイの `.env` (`N8N_TASKS_LIST_URL`) に設定

## 1. 環境設定とモデルの定義

- [x] 1.1 `.env.example` およびローカルの `.env` に `N8N_TASKS_LIST_URL` を追加
- [x] 1.2 `src/core/config.py` の `Settings` クラスに `N8N_TASKS_LIST_URL` を追加
- [x] 1.3 `src/api/models.py` に `TasksGroup` および `ListOption` Pydantic モデルを追加し、`DsgCommandData` を拡張

## 2. サービス層の実装

- [x] 2.1 `src/services/n8n.py` に `get_tasks_list()` メソッドを追加し、n8n Webhook から Markdown 文字列を取得する処理を実装

## 3. コマンド登録とハンドラの追加

- [x] 3.1 `src/cli/register_commands.py` に `/dsg tasks list` コマンドの定義を追加
- [x] 3.2 `src/api/handlers.py` に `handle_dsg_tasks_list` ハンドラを追加。Discord の Type 5 (Deferred Response) を返却するように実装
- [x] 3.3 `src/api/handlers.py` にバックグラウンド処理用の `update_tasks_list_background` 関数を追加。n8n からデータを取得し、Discord Webhook を介してメッセージを PATCH 更新する処理を実装
- [x] 3.4 `src/api/handlers.py` の `handle_dsg_command` に新コマンドの振り分けロジックを追加

## 4. 動作確認とテスト

- [ ] 4.1 `scripts/dev.sh` 等を使用してローカル環境を起動し、コマンドが Discord に正しく登録されるか確認
- [ ] 4.2 `/dsg tasks list` を実行し、即座に「考え中...」が表示され、その後 n8n からの結果で更新されることを確認
- [x] 4.3 `tests/` に新しいコマンドと非同期処理のテストケースを追加
