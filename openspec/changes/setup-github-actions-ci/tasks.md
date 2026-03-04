## 1. GitHub Actions ワークフローの作成

- [ ] 1.1 `.github/workflows/` ディレクトリを作成する
- [ ] 1.2 `.github/workflows/python-checks.yaml` を作成し、基本的な構造（トリガー、ジョブ定義）を記述する

## 2. Python 品質チェックジョブの実装

- [ ] 2.1 `astral-sh/setup-uv` を使用した Python 環境のセットアップ手順を記述する
- [ ] 2.2 依存関係のインストール (`uv sync --frozen`) 手順を記述する
- [ ] 2.3 Ruff による Lint チェック (`uv run ruff check .`) ステップを追加する
- [ ] 2.4 Ruff によるフォーマットチェック (`uv run ruff format --check .`) ステップを追加する
- [ ] 2.5 Mypy による型チェック (`uv run mypy .`) ステップを追加する
- [ ] 2.6 Pytest によるテスト実行 (`uv run pytest`) ステップを追加する

## 3. Docker ビルドチェックジョブの実装

- [ ] 3.1 Docker イメージのビルド (`docker build .`) ステップをワークフローに追加する

## 4. 動作検証

- [ ] 4.1 ワークフローファイルをプッシュし、GitHub Actions 上でジョブが正常に実行・完了することを確認する
