## Why

Discord の Interaction Endpoint URL を固定しつつ、開発環境（ngrok）への自動転送を実現することで、Developer Portal の設定変更に伴う手間とミスを排除するため。また、GitHub Release をトリガーとした自動デプロイを構築し、本番環境への安全かつ迅速な反映を可能にします。

## What Changes

- Cloud Run を「署名検証プロキシ」として動作させるロジックの実装（`MODE=dev` 時のフォワード機能）。
- ローカルの `docker compose` の起動・停止に連動して Cloud Run のモードを自動で切り替えるオートメーションスクリプトの導入。
- GitHub Actions を使用した、リリース・タグをトリガーとする Cloud Run への継続的デリバリー（CD）パイプラインの構築。
- Google Cloud のセキュリティ設定（Workload Identity Federation）を自動化するセットアップスクリプトの提供。

## Capabilities

### New Capabilities
- `cloud-run-proxy`: Cloud Run 側での署名検証および、開発環境への透過的なリクエスト転送機能。
- `ci-cd-pipeline`: GitHub Actions による Docker イメージビルドと Cloud Run への自動デプロイフロー。
- `local-dev-automation`: `docker compose` のライフサイクルに合わせた Cloud Run の `MODE` 切り替え自動化。

### Modified Capabilities
- `interaction-endpoint`: エンドポイントの振る舞いに、転送（Proxy）という選択肢を追加。

## Impact

- `src/api/routes.py`, `src/api/deps.py`: フォワードロジックの追加。
- `src/core/config.py`: `MODE` や `FORWARD_URL` などの新規設定項目。
- `scripts/`: GCP セットアップおよびモード切替用の新規スクリプト。
- `.github/workflows/`: デプロイ用ワークフローの追加。
- `Dockerfile`: Cloud Run 向けのポート設定等の調整。
