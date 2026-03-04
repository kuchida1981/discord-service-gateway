## Purpose

OpenSpec の設計原則および運用ルールに基づき、ドキュメントの整合性が保たれていること、および変更内容が適切にアーカイブされた上でマージされることを自動検証することを目的とする。

## Requirements

### Requirement: OpenSpec Document Integrity
すべての OpenSpec ドキュメント（changes, specs, artifacts）は、構文および構造上の整合性が保たれていなければならない (SHALL)。
`npx openspec validate --strict --all` コマンドを使用して、欠落しているアーティファクトや不正な定義を検出しなければならない。

#### Scenario: Running strict validation
- **WHEN** `openspec validate --strict --all` を実行する
- **THEN** ドキュメントの不備やスキーマ違反が検出されてはならない

### Requirement: Change Archive Enforcement
すべての PR は、マージ前に変更内容をアーカイブしていなければならない (SHALL)。
`openspec/changes/` ディレクトリ内に、アーカイブされていないアクティブな変更が存在してはならない。

#### Scenario: Ensure all changes are archived
- **WHEN** `openspec/changes/` ディレクトリ内のファイルを走査し、`archive` 以外のディレクトリを検出する
- **THEN** 隠しファイルを除き、アクティブな変更ディレクトリが見つかってはならない

### Requirement: Implementation Verification
すべての変更は、マージ前にその実装がアーティファクトと一致していることが検証されていなければならない (SHALL)。
`npx openspec verify` 等の整合性検証が必要に応じて実行されなければならない。
