## Context

現在のプロジェクトでは、`scripts/` ディレクトリに Python スクリプト（`register_commands.py`, `toggle_mode.py`）が配置されています。これらは `src/` 配下のコード（特に `src/core/config.py`）に依存していますが、パッケージ外にあるため、実行時に `PYTHONPATH` を手動で調整する必要があったり、IDE や静的解析ツールが依存関係を正しく認識できないという課題があります。

## Goals / Non-Goals

**Goals:**
- Python スクリプトを `src/` パッケージ内に集約し、依存関係の解決を簡素化する。
- `uv` の機能を利用して、スクリプトをプロジェクトのコマンド（`project.scripts`）として定義し、実行を標準化する。
- `scripts/dev.sh` などの既存のワークフローを維持しつつ、内部的な呼び出しを `uv run` に移行する。
- `src/` 配下に適用されている Ruff や Mypy の厳格なルールを、ツール類にも一貫して適用する。

**Non-Goals:**
- スクリプトのロジック自体のリファクタリング（挙動の変更は行わない）。
- シェルスクリプト（`.sh`）の `src/` への移動（これらは引き続き `scripts/` に残す）。

## Decisions

1. **ディレクトリ構成の変更**: `src/cli/` を新設し、そこに Python スクリプトを配置する。`__init__.py` を作成し、パッケージとして認識させる。
2. **`pyproject.toml` への登録**: `[project.scripts]` セクションに以下を登録する。
   - `register-commands = "src.cli.register_commands:register_commands"`
   - `toggle-mode = "src.cli.toggle_mode:main"`
3. **`dev.sh` の呼び出し修正**: `python3 scripts/toggle_mode.py` の直接呼び出しを、`uv run toggle-mode` に変更する。
4. **Dockerfile の最適化**: `src/` のコピーに Python ツールが含まれるようになるため、Docker イメージ内でも `uv run` を介したツールの実行が可能になる。

## Risks / Trade-offs

- **[Risk] インポートパスの不整合** → `src/cli/` に移動することで、相対インポートではなく絶対インポート (`from src.core...`) を標準とする。
- **[Risk] 実行パスの変更による混乱** → 移行後、旧パスのファイルは削除し、`uv run` を推奨する旨を README 等で周知する（今回のスコープでは `dev.sh` の修正で対応）。
