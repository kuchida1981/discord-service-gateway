## Why
現在、コードベース内に 20 箇所以上の `noqa` コメントが散在しており、技術的負債および可読性の低下を招いています。これらの多くは特定のファイルやディレクトリにおいて正当な理由があるものですが、個別の行にコメントを記述するのではなく、Ruff の設定（`pyproject.toml`）で一括管理することで、コードをクリーンに保ち、プロジェクトの Lint ポリシーを明文化します。

## What Changes
- **Ruff 設定の整理**: `pyproject.toml` の `per-file-ignores` セクションを更新し、CLI ツールやテストコード、設定ファイルにおける特定の警告（`T201`, `S105`, `S603`, `S104`）をディレクトリ単位で許容するように変更します。
- **コードのリファクタリング**: 
    - `TRY400`: `logger.error` を `logger.exception` または `logger.warning` に書き換え、不適切な例外処理の警告を解消します。
    - `TRY003`: 独自例外クラスを導入し、例外メッセージの長大化による警告を解消します。
- **noqa コメントの全削除**: 上記の設定とリファクタリング完了後、プロジェクト全体から `noqa` コメントを一括削除します。

## Capabilities

### New Capabilities
- なし

### Modified Capabilities
- `quality-assurance`: プロジェクト全体の Lint ルールおよびコード品質の維持方針を、インラインの `noqa` から設定ベースの管理に移行し、より厳格かつ透明性の高い運用に変更します。特に、CLI ツールにおける `print` の許容など、コンテキストに応じたルール適用を明文化します。

## Impact
- `pyproject.toml`: Ruff 設定の変更。
- `src/cli/`: `print` および `subprocess` の使用に関する `noqa` の削除。
- `src/api/deps.py`: 例外ハンドリングの修正。
- `src/core/config.py`: トークンデフォルト値に関する `noqa` の削除。
- `tests/`: テスト用モックトークンに関する `noqa` の削除。
