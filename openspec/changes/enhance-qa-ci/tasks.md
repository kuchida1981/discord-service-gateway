## 1. 既存ワークフローの修正 (Draft 制御)

- [ ] 1.1 `.github/workflows/python-checks.yaml` の `on.pull_request.types` に `ready_for_review` を追加する
- [ ] 1.2 `python-checks.yaml` の各ジョブ（lint, type-check, test, docker-build）に `if: github.event.pull_request.draft == false` を追加する

## 2. 新規ワークフローの作成 (OpenSpec 整合性)

- [ ] 2.1 `.github/workflows/check-openspec.yml` を新規作成する
- [ ] 2.2 OpenSpec のインストール (`npm install -g`) と `validate --strict --all` ステップを実装する
- [ ] 2.3 アーカイブされていない変更を検出するシェルスクリプトステップを実装する
- [ ] 2.4 ジョブに `if: github.event.pull_request.draft == false` を追加する

## 3. 新規ワークフローの作成 (PR メタデータ)

- [ ] 3.1 `.github/workflows/check-pr-issue.yml` を新規作成し、`github-script` による Issue 紐付けチェックを実装する
- [ ] 3.2 `check-pr-issue.yml` に `if: github.event.pull_request.draft == false` を追加する
- [ ] 3.3 `.github/workflows/check-todo.yml` を新規作成し、Draft PR でも実行されるように `if` 条件なしで実装する

## 4. 動作検証

- [ ] 4.1 Draft PR を作成し、`check-todo` のみが実行されることを確認する
- [ ] 4.2 PR を Ready for Review に切り替え、すべてのチェックが実行・パスすることを確認する
