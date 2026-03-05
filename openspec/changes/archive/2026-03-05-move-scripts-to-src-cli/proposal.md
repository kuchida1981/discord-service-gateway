## Why

現在の `scripts/` 配下の Python ファイル（`register_commands.py`, `toggle_mode.py`）は、アプリケーションの設定（`src/core/config.py`）に依存しているにもかかわらず、`src` パッケージの外に配置されています。これにより、インポートの解決が複雑になり、Lint（Ruff）や型チェック（Mypy）の対象からも外れやすくなっています。

これらのファイルを `src/cli/` 配下に移動し、`pyproject.toml` の `project.scripts` として登録することで、開発・運用ツールの管理を簡素化し、コード品質の統一を図ります。

## What Changes

- **Python スクリプトの移動**: `scripts/register_commands.py` および `scripts/toggle_mode.py` を `src/cli/` ディレクトリに移動します。
- **パッケージ構成の更新**: `src/cli/__init__.py` を作成し、ディレクトリをパッケージ化します。
- **エントリポイントの登録**: `pyproject.toml` に `register-commands` と `toggle-mode` のコマンドを登録し、`uv run <command>` で実行可能にします。
- **ラッパースクリプトの修正**: `scripts/dev.sh` 内の Python 呼び出しを `uv run toggle-mode` に変更します。
- **デプロイ設定の整理**: `Dockerfile` を更新し、`src/` 配下に集約されたツールを利用するように最適化します。

## Capabilities

### New Capabilities
- `cli-tooling`: 開発およびデプロイ環境の操作を標準化された CLI コマンド（`uv run` 経由）として提供します。

### Modified Capabilities
- (なし)

## Impact

- `src/cli/`: 新しいディレクトリとスクリプトが追加されます。
- `scripts/`: Python ファイルが削除され、シェルスクリプトのみになります。
- `pyproject.toml`: 新しいスクリプトエントリポイントが追加されます。
- `Dockerfile`: `COPY scripts/` の扱いが変更または削除されます。
