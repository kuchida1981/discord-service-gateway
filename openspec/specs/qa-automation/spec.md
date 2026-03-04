## Purpose

プルリクエスト（PR）作成からマージまでの過程において、プロジェクトの運用ルール（Issueとの紐付け、タスクの完遂）が遵守されていることを自動的に検証し、トレーサビリティと品質を確保することを目的とする。

## Requirements

### Requirement: Issue Linking
すべての PR は、関連する Issue と紐付けられていなければならない (SHALL)。
PR のタイトルまたは本文（説明欄）に、Issue 番号（`#123` 形式）が含まれていなければならない。

#### Scenario: Verify issue link existence
- **WHEN** PR のタイトルまたは本文を正規表現 `/#\d+/` で検索する
- **THEN** 少なくとも 1 つのマッチが見つからなければならない

### Requirement: Task Completion (TODO Checklist)
PR の説明欄に含まれるチェックリスト（`- [ ]` 形式）は、マージ前にすべて完了（`- [x]` 形式）していなければならない (SHALL)。
未完了のタスクが残っている場合、CI は失敗しなければならない。

#### Scenario: Check for pending TODO items
- **WHEN** PR の説明欄からコードブロックを除外したテキストを走査する
- **THEN** `^([[:space:]]*)?- \[ \]` にマッチする行が存在してはならない

### Requirement: Early Traceability
Issue 紐付けの検証は、PR が Draft 状態であっても実行されなければならない (SHALL)。
これにより、開発の初期段階から関連する Issue が明確に定義されていることを保証し、トレーサビリティを向上させる。

#### Scenario: Continuous traceability check
- **WHEN** PR が Draft 状態であっても、タイトルまたは本文が更新される
- **THEN** 即座に Issue 番号の有無が検証されなければならない
