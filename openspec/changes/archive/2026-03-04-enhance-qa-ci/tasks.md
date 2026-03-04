## 1. 既存ワークフローの修正 (Draft 制御)

- [x] 1.1 `.github/workflows/python-checks.yaml` の `on.pull_request.types` に `ready_for_review` を追加する
- [x] 1.2 `python-checks.yaml` の各ジョブ（lint, type-check, test, docker-build）に `if: github.event.pull_request.draft == false` を追加する

## 2. 新規ワークフローの作成 (OpenSpec 整合性)

- [x] 2.1 `.github/workflows/check-openspec.yml` を新規作成する
- [x] 2.2 OpenSpec のインストール (`npm install -g`) と `validate --strict --all` ステップを実装する
- [x] 2.3 アーカイブされていない変更を検出するシェルスクリプトステップを実装する
- [x] 2.4 ジョブに `if: github.event.pull_request.draft == false` を追加する

## 3. 新規ワークフローの作成 (PR メタデータ)

- [x] 3.1 `.github/workflows/check-pr-issue.yml` を新規作成し、`github-script` による Issue 紐付けチェックを実装する
- [x] 3.2 `check-pr-issue.yml` を Draft PR でも実行されるように `if` 条件なしで実装する
- [x] 3.3 `.github/workflows/check-todo.yml` を新規作成し、`if: github.event.pull_request.draft == false` を追加する

## 4. 動作検証

- [x] 4.1 Draft PR を作成し、`check-pr-issue` のみが実行されることを確認する
- [x] 4.2 PR を Ready for Review に切り替え、すべてのチェックが実行・パスすることを確認する
