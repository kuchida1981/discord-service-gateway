## 1. toggle_mode.py の機能拡張

- [ ] 1.1 `SYNC_ENV_VARS` 定数の定義と環境変数の読み込みロジックの追加
- [ ] 1.2 `toggle_mode` 関数に環境変数の同期ロジック（`--update-env-vars` の構築）を追加
- [ ] 1.3 現在の設定（Cloud Run 側とローカル側）を比較表示するステータス取得機能の追加

## 2. dev.sh の改善

- [ ] 2.1 `.env` と `.env.example` のキーを比較し、不足を警告するバリデーション機能の追加
- [ ] 2.2 `.env` のハッシュ値（MD5）を算出し、環境変数 `ENV_HASH` としてエクスポートするロジックの追加
- [ ] 2.3 `status` コマンドの実装（`uv run toggle-mode status` の呼び出し等）
- [ ] 2.4 `up` コマンド実行時に `toggle-mode` の同期機能を呼び出すよう修正

## 3. Docker 設定の修正

- [ ] 3.1 `docker-compose.yml` の `app` サービスに `ENV_HASH` 環境変数を追加し、設定変更を検知可能にする

## 4. 動作確認と検証

- [ ] 4.1 `dev.sh status` で同期状況が正しく表示されることを確認
- [ ] 4.2 `.env` 内の `DISCORD_PUBLIC_KEY` 等を書き換えた際、`dev.sh up` で Cloud Run 側も更新されることを確認
- [ ] 4.3 `.env` 変更後に `dev.sh up` を実行すると Docker コンテナが再作成されることを確認
