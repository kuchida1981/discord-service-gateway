## 1. 準備とディレクトリ作成

- [ ] 1.1 `src/cli/` ディレクトリを作成する
- [ ] 1.2 `src/cli/__init__.py` を作成し、パッケージ化する

## 2. スクリプトの移動と調整

- [ ] 2.1 `scripts/register_commands.py` を `src/cli/` に移動し、インポートパスを修正する
- [ ] 2.2 `scripts/toggle_mode.py` を `src/cli/` に移動する
- [ ] 2.3 `scripts/__init__.py` を削除する（不要になるため）

## 3. プロジェクト設定の更新

- [ ] 3.1 `pyproject.toml` の `[project.scripts]` に `register-commands` と `toggle-mode` を追加する
- [ ] 3.2 `uv sync` を実行してエントリポイントを反映させる

## 4. 既存スクリプトと設定の修正

- [ ] 4.1 `scripts/dev.sh` 内の `toggle_mode.py` 呼び出しを `uv run toggle-mode` に置き換える
- [ ] 4.2 `Dockerfile` から `COPY scripts/` を削除、または Python ファイルのコピーを停止するよう調整する

## 5. 検証とクリーンアップ

- [ ] 5.1 `uv run register-commands --help` が正常に動作することを確認する
- [ ] 5.2 `uv run toggle-mode --help` が正常に動作することを確認する
- [ ] 5.3 `ruff check src/cli` および `mypy src/cli` を実行し、品質基準を満たしていることを確認する
- [ ] 5.4 `scripts/` 配下の不要になった Python ファイルが削除されていることを確認する
