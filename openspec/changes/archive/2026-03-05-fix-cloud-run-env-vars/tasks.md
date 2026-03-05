## 1. ワークフローの修正

- [x] 1.1 `.github/workflows/deploy.yml` の `gcloud run deploy` ステップに環境変数の追加
- [x] 1.2 `DISCORD_TOKEN`, `DISCORD_APPLICATION_ID`, `DISCORD_GUILD_ID` を `--set-env-vars` に含める

## 2. 検証

- [x] 2.1 ワークフローの構文チェック
- [x] 2.2 GitHub Secrets の設定依頼（必要項目の確認）
- [ ] 2.3 `workflow_dispatch` またはリリースタグ作成によるデプロイの実行確認
