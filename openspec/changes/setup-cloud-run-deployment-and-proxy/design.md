## Context

Discord Interaction Endpoint を Cloud Run で運用する際、開発環境（ローカル）へのスムーズなリクエスト転送と、セキュアかつ自動化されたデプロイパイプラインが必要。

## Goals / Non-Goals

**Goals:**
- Cloud Run を「署名検証プロキシ」として機能させ、開発中のみ ngrok 経由でローカルへ転送する。
- `git tag` によるリリースをトリガーに、GitHub Actions で Cloud Run へ自動デプロイする。
- Workload Identity Federation (WIF) を使用し、GitHub Actions に GCP の永続的な鍵を持たせない。
- ローカルの `docker compose` 起動・停止に連動して、Cloud Run の `MODE` を自動で切り替える。

**Non-Goals:**
- Cloud Run 以外（Lambda, App Engine 等）へのデプロイ。
- 複数人の開発者が同時に同じ Cloud Run インスタンスを「開発モード」で奪い合う競合の解決（当面は個人開発を想定）。

## Decisions

### 1. 署名検証の集約
- **決定**: 署名検証は Cloud Run (Proxy) でのみ行い、ローカルは `MODE=local` 設定時に検証をスキップする。
- **理由**: 公開鍵をローカルに持たせる手間を省き、セキュリティの境界をクラウド側に固定できるため。

### 2. リクエスト転送の実装
- **決定**: FastAPI の `Depends` を拡張し、署名検証済みの `bytes` ボディをそのまま `httpx` で転送する。
- **理由**: Middleware よりも依存注入の方が、特定のルート（`/interactions`）に限定したロジックを書きやすく、リクエストボディの再利用も容易なため。

### 3. モード切替の自動化
- **決定**: Python スクリプト (`scripts/toggle_mode.py`) を作成し、`gcloud run services update` で環境変数のみを更新する。
- **理由**: コンテナの再ビルドを伴わないため、切り替えが数十秒で完了し、開発のテンポを損なわない。環境変数の更新により新しいリビジョンが作成されるが、イメージのビルドがないため高速である。

### 4. CI/CD 認証
- **決定**: Google Cloud の Workload Identity Federation (WIF) を採用。
- **理由**: GitHub Secrets に JSON 鍵を保存する従来の方法よりセキュアで、鍵の管理・更新コストが低いため。

## Risks / Trade-offs

- **[Risk] 3秒ルールへの抵触** → [Mitigation] 開発中は `PONG` (Type 1) 以外の重い処理を非同期（Followup）へ移行することを推奨。また、ngrok のレイテンシを最小化するため、リージョンを合わせる。
- **[Risk] Cloud Run の切り替え忘れ** → [Mitigation] `docker compose down` 時に自動で `MODE=prod` に戻すスクリプトを仕込むが、万一のために手動復旧コマンドも `README` に明記する。
- **[Risk] 新リビジョン作成のオーバーヘッド** → [Mitigation] 数十秒の反映待ちは発生するが、手動での URL 変更の手間とリスクを天秤にかけ、許容範囲内と判断。

## Migration Plan

1. WIF 設定用スクリプトをユーザーが実行し、GCP 環境を整備。
2. GitHub Actions ワークフローを push し、最初のデプロイを成功させる。
3. ローカルの `docker compose` 設定を更新し、スイッチ機能を有効化する。
