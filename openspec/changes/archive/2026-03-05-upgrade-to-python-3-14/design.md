## Context

現在の Python 3.11 環境から、最新の安定版である Python 3.14 へシステム全体をアップグレードする。パッケージ管理には `uv` を使用しており、コンテナベースのデプロイ（Cloud Run）を行っている。

## Goals / Non-Goals

**Goals:**
- システム全体の Python ランタイムを 3.14 に統一する。
- 全ての CI/CD パイプラインが Python 3.14 で正常に動作することを確認する。
- 既存の全テストが Python 3.14 環境でパスすることを確認する。

**Non-Goals:**
- GIL フリー（Free-threaded）モードの有効化（今回は標準ビルドを使用）。
- Python 3.14 の新機能（t-strings 等）を用いた大規模なリファクタリング（互換性確認を優先）。

## Decisions

### 1. ベースイメージの選定
- **Decision**: `ghcr.io/astral-sh/uv:python3.14-bookworm-slim` を使用する。
- **Rationale**: 現在 3.11 で使用しているイメージの最新版であり、`uv` がプリインストールされているためビルドが高速。
- **Alternatives**: `python:3.14-slim` に手動で `uv` を入れる構成も検討したが、メンテナンスコストを考え公式イメージを継続。

### 2. 依存関係の更新方針
- **Decision**: `uv lock --upgrade` を実行して、全ての依存関係を 3.14 向けにリフレッシュする。
- **Rationale**: Python バージョン変更に伴い、最適なバイナリ（Wheels）が提供されている可能性があるため。特に `pynacl` は 1.6.2 以上が必須。

### 3. Ruff/Mypy のターゲットバージョン
- **Decision**: `pyproject.toml` 内のターゲットを `py314` に設定する。
- **Rationale**: 3.14 固有の構文チェックや型チェックを有効にするため。

## Risks / Trade-offs

- **[Risk]** 一部のサードパーティライブラリが Python 3.14 で未検証または非互換である可能性。
  - **Mitigation**: `uv lock` 時の依存関係解決を確認し、全ユニットテストを実行して検証する。
- **[Risk]** Docker イメージサイズの変化。
  - **Mitigation**: `slim` イメージを使用し、不要なキャッシュを削除することで最小化を維持する。
