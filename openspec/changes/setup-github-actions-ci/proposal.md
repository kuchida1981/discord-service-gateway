## Why

プロジェクトの品質を維持し、プルリクエスト時のデグレを自動的に防ぐための継続的インテグレーション（CI）環境を構築します。現状、品質チェック（Lint, テスト, 型チェック）は手動実行に依存しており、CI による自動化されたガードレールを導入することで、開発速度とコード品質の両立を図ります。

## What Changes

- GitHub Actions ワークフロー (`.github/workflows/python-checks.yaml`) の追加。
- `astral-sh/setup-uv` を使用した Python 依存関係の高速なセットアップとキャッシュ。
- `ruff check`, `ruff format --check`, `mypy`, `pytest` の自動実行パイプラインの構築。
- `Dockerfile` のビルド可能性を検証する Docker ビルドチェックの追加。

## Capabilities

### New Capabilities
- `continuous-integration`: プルリクエストおよび main ブランチへのプッシュ時に、定義された品質チェックを自動実行するパイプライン。
- `docker-build-verification`: 変更によって Docker イメージのビルドが壊れていないことを CI 上で保証する仕組み。

### Modified Capabilities
- `quality-assurance`: 定義済みの品質基準（Lint, テスト, 型チェック）が、CI 環境において自動的に検証されるべきであるという要件を追記。

## Impact

- **GitHub リポジトリ**: `.github/workflows/` ディレクトリ配下に設定ファイルが追加されます。
- **開発ワークフロー**: プルリクエスト作成時に自動チェックが走り、パスしない場合はマージがブロックされるようになります。
- **依存関係**: `astral-sh/setup-uv` アクションへの依存が発生します。
