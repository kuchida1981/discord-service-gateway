## MODIFIED Requirements

### Requirement: GitHub Actions Based Deployment
システムは、GitHub のリリースタグが作成された際に、Cloud Run への自動デプロイを開始しなければならない (SHALL)。デプロイされるイメージは Python 3.14 ベースでなければならない。さらに、デプロイ時にはアプリケーションの実行に必要なすべての環境変数（`DISCORD_TOKEN`, `DISCORD_APPLICATION_ID`, `DISCORD_PUBLIC_KEY`, `DISCORD_GUILD_ID`, `MODE`）が正しく注入されなければならない (SHALL)。

#### Scenario: Successful release deployment with env vars
- **WHEN** ユーザーが GitHub 上で `*.*.*` 形式のタグを作成し、リリースを公開する
- **THEN** GitHub Actions がトリガーされ、Docker イメージのビルド・プッシュ後、必要なすべての環境変数が設定された状態で Cloud Run へのデプロイが完了しなければならない
