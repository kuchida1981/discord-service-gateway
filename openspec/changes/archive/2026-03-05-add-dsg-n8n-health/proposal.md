## Why

Discord Service Gateway (DSG) として、複数の外部サービスや機能を統合管理するための整理されたインターフェースが必要です。
個別のコマンドが散在するのを防ぎ、`/dsg <service> <action>` という階層的な名前空間を導入することで、将来的な拡張性とユーザーの使いやすさを確保します。

## What Changes

- **新しいコマンド体系の導入**: `/dsg` をトップレベルコマンドとし、サブコマンドグループによって機能を分類する構造を導入します。
- **n8n ヘルスチェックコマンドの実装**: `/dsg n8n health` コマンドを追加し、n8n インスタンスの状態（`https://n8n.u-rei.com/healthz`）を確認できるようにします。
- **既存コマンドの整理**: 現状の `ping` コマンドを、新しい体系に合わせて `/dsg utils ping` （仮）などへ移行するための基盤を整えます。

## Capabilities

### New Capabilities
- `dsg-command-infrastructure`: スラッシュコマンドの階層構造（サブコマンドグループ、サブコマンド）を定義・登録・処理するための基盤機能。
- `n8n-integration`: n8n サービスとの連携機能。第一段階としてヘルスチェック（status確認）を含みます。

### Modified Capabilities
- `slash-commands`: 既存のコマンド登録ロジックを、階層構造に対応させるために拡張します。

## Impact

- `src/cli/register_commands.py`: コマンド定義の構造変更。
- `src/api/routes.py`: インタラクション受信時のルーティングロジックの変更。
- `src/core/config.py`: n8n のエンドポイントURL等の設定追加。
