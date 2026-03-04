## Context
既存の `python-checks.yaml` は、プルリクエスト（PR）作成時に常に実行されますが、開発初期の Draft PR 段階では、Lint やテストがパスしないことが想定されるため、これらのチェックは Ready for Review になってから実行するのが効率的です。一方で、PR が正しい Issue と紐付けられているかは、初期段階から可視化されるべき重要なトレーサビリティ要件です。

## Goals / Non-Goals

**Goals:**
- 各品質チェックワークフローに Draft PR 時のスキップロジックを導入する。
- `check-pr-issue.yml` のみを Draft PR 段階でも実行される唯一のワークフローとする。
- Python プロジェクト環境で OpenSpec の整合性とアーカイブ状況を自動検証する。
- PR のタイトルまたは本文に Issue 番号が含まれていることを保証する。

**Non-Goals:**
- `package.json` を新規作成すること（既存の Python/uv 構成を維持する）。
- PR と実際の Issue のステータスを同期させるなどの高度な連携。

## Decisions

- **Draft PR スキップの条件判定**
  - ジョブレベルの `if: github.event.pull_request.draft == false` を採用します。これにより、Draft 段階ではジョブ自体が起動せず、リソースを節約できます。
  - トリガーには `ready_for_review` を追加し、ステータス変更時に自動的に CI が走るようにします。

- **OpenSpec のインストール (Python 環境)**
  - `package.json` がないため、`npm install -g @fission-ai/openspec@latest` を使用して OpenSpec CLI をセットアップします。`npx` で毎回フェッチするよりも、明示的にインストールするステップを分けることで、キャッシュやエラーハンドリングを制御しやすくします。

- **Issue チェックのロジック**
  - `actions/github-script` を使用し、タイトルと本文の両方を対象に正規表現 `/#\d+/` で検索します。リファレンスの実装をそのまま踏襲し、Draft 段階でも実行することで早期の紐付けを促します。

- **TODO チェックのロジック**
  - `grep -qE '^([[:space:]]*)?- \[ \]'` を使用して、未チェックの項目を検出します。リファレンスの実装を踏襲しつつ、Draft 段階ではスキップするように設定します。

## Risks / Trade-offs

- **[Risk] Ready for Review になった瞬間に大量の CI が走る** → **[Mitigation]** 並列実行されるため、開発者へのフィードバックは速やかに得られます。
- **[Risk] OpenSpec CLI のバージョン不一致** → **[Mitigation]** `@latest` を指定することで、常に最新の検証ルールを適用します。
