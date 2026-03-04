## 1. GCP 準備 & 認証設定

- [x] 1.1 WIF (Workload Identity Federation) セットアップ用スクリプトの作成 (`scripts/setup_gcp.sh`)
- [x] 1.2 ユーザーによる GCP プロジェクトでのスクリプト実行と GitHub Secrets の登録
- [x] 1.3 Cloud Run / Artifact Registry / IAM API の有効化確認

## 2. アプリケーション・コアの実装

- [x] 2.1 `src/core/config.py` への `MODE`, `FORWARD_URL`, `PROXY_SECRET` 設定の追加
- [x] 2.2 `src/api/deps.py` の署名検証ロジックを `MODE=local` でスキップ可能に修正
- [x] 2.3 `src/api/routes.py` または依存関係への、`MODE=dev` 時のフォワード処理の実装

## 3. デプロイ & ライフサイクル自動化

- [x] 3.1 GitHub Actions デプロイワークフロー (`.github/workflows/deploy.yml`) の作成
- [x] 3.2 モード切替用 Python スクリプト (`scripts/toggle_mode.py`) の作成
- [x] 3.3 `docker compose` の起動・停止に連動するラッパースクリプト (`scripts/dev.sh`) の作成
- [x] 3.4 `Dockerfile` の Cloud Run 向け調整（ポート設定の動的対応など）

## 4. 疎通確認 & テスト

- [ ] 4.1 `git tag` による初回のデプロイ成功の確認
- [x] 4.2 ローカル起動時の Cloud Run モード自動切替の動作確認
- [x] 4.3 Cloud Run (Proxy) -> Local (ngrok) 経由での Interaction 受信テスト
