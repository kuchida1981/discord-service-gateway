## MODIFIED Requirements

### Requirement: GitHub Actions Based Deployment
システムは、GitHub のリリースタグが作成された際に、Cloud Run への自動デプロイを開始しなければならない (SHALL)。デプロイされるイメージは Python 3.14 ベースでなければならない。

#### Scenario: Successful release deployment
- **WHEN** ユーザーが GitHub 上で `v*.*.*` 形式のタグを作成し、リリースを公開する
- **THEN** GitHub Actions がトリガーされ、Python 3.14 ベースの Docker イメージのビルド、プッシュ、および Cloud Run へのデプロイが完了しなければならない
