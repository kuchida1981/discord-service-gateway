## Purpose

リリースタグの作成をトリガーとした、Cloud Run への安全かつ自動化されたデプロイパイプラインの仕様を定義する。

## Requirements

### Requirement: GitHub Actions Based Deployment
システムは、GitHub のリリースタグが作成された際に、Cloud Run への自動デプロイを開始しなければならない (SHALL)。デプロイされるイメージは Python 3.14 ベースでなければならない。

#### Scenario: Successful release deployment
- **WHEN** ユーザーが GitHub 上で `v*.*.*` 形式のタグを作成し、リリースを公開する
- **THEN** GitHub Actions がトリガーされ、Python 3.14 ベースの Docker イメージのビルド、プッシュ、および Cloud Run へのデプロイが完了しなければならない

### Requirement: Workload Identity Federation (WIF) Authentication
GitHub Actions から Google Cloud への認証は、長期的な JSON キーを使用せず、WIF を使用して一時的な認証トークンを取得しなければならない (SHALL)。

#### Scenario: Authenticate with WIF
- **WHEN** デプロイワークフローが開始される
- **THEN** GitHub Actions は構成された WIF プロバイダーを使用して GCP のデプロイ用サービスアカウントになりすまし、認証を完了しなければならない
