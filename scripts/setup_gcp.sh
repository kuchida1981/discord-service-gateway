#!/bin/bash
# WIF (Workload Identity Federation) セットアップスクリプト
# GitHub Actions から Cloud Run へデプロイするための認証設定を自動化

set -euo pipefail

# 色付きログ
info() { echo -e "\033[0;34m[INFO]\033[0m $*"; }
success() { echo -e "\033[0;32m[SUCCESS]\033[0m $*"; }
error() { echo -e "\033[0;31m[ERROR]\033[0m $*"; exit 1; }

# 必須環境変数の確認
: "${PROJECT_ID:?環境変数 PROJECT_ID が必要です}"
: "${REGION:=asia-northeast1}"  # デフォルトは東京リージョン
: "${SERVICE_NAME:=discord-gateway}"
: "${GITHUB_REPO:?環境変数 GITHUB_REPO が必要です (例: username/repo)}"

info "Setting up WIF for project: $PROJECT_ID"
info "GitHub Repo: $GITHUB_REPO"
info "Region: $REGION"
info "Service Name: $SERVICE_NAME"

# API の有効化
info "Enabling required GCP APIs..."
# Note: cloudresourcermanager.googleapis.com は gcloud CLI から有効化できない場合があります
# その場合は GCP Console から手動で有効化してください
if gcloud services enable \
  run.googleapis.com \
  artifactregistry.googleapis.com \
  iamcredentials.googleapis.com \
  --project="$PROJECT_ID" 2>/dev/null; then
  success "APIs enabled"
else
  warn "API の自動有効化に失敗しました"
  warn "GCP Console から手動で以下の API を有効化してください:"
  warn "  - Cloud Run Admin API"
  warn "  - Artifact Registry API"
  warn "  - IAM Service Account Credentials API"
  warn "URL: https://console.cloud.google.com/apis/library?project=$PROJECT_ID"
  read -p "API を有効化しましたか？ (y/N): " -n 1 -r
  echo
  if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    error "API の有効化が必要です"
  fi
fi

# Artifact Registry リポジトリの作成
REPO_NAME="discord-gateway"
info "Creating Artifact Registry repository: $REPO_NAME"
if gcloud artifacts repositories describe "$REPO_NAME" \
  --location="$REGION" \
  --project="$PROJECT_ID" &>/dev/null; then
  info "Repository already exists, skipping..."
else
  gcloud artifacts repositories create "$REPO_NAME" \
    --repository-format=docker \
    --location="$REGION" \
    --project="$PROJECT_ID"
  success "Artifact Registry repository created"
fi

# サービスアカウントの作成
SA_NAME="github-actions-deployer"
SA_EMAIL="${SA_NAME}@${PROJECT_ID}.iam.gserviceaccount.com"

info "Creating service account: $SA_NAME"
if gcloud iam service-accounts describe "$SA_EMAIL" \
  --project="$PROJECT_ID" &>/dev/null; then
  info "Service account already exists, skipping..."
else
  gcloud iam service-accounts create "$SA_NAME" \
    --display-name="GitHub Actions Deployer" \
    --project="$PROJECT_ID"
  success "Service account created"
fi

# サービスアカウントへのロール付与
info "Granting roles to service account..."
for role in \
  "roles/run.admin" \
  "roles/iam.serviceAccountUser" \
  "roles/artifactregistry.writer"; do
  gcloud projects add-iam-policy-binding "$PROJECT_ID" \
    --member="serviceAccount:${SA_EMAIL}" \
    --role="$role" \
    --condition=None \
    --quiet
done
success "Roles granted"

# Workload Identity Pool の作成
POOL_NAME="github-pool"
info "Creating Workload Identity Pool: $POOL_NAME"
if gcloud iam workload-identity-pools describe "$POOL_NAME" \
  --location="global" \
  --project="$PROJECT_ID" &>/dev/null; then
  info "Pool already exists, skipping..."
else
  gcloud iam workload-identity-pools create "$POOL_NAME" \
    --location="global" \
    --display-name="GitHub Actions Pool" \
    --project="$PROJECT_ID"
  success "Workload Identity Pool created"
fi

# Workload Identity Provider の作成
PROVIDER_NAME="github-provider"
info "Creating Workload Identity Provider: $PROVIDER_NAME"
if gcloud iam workload-identity-pools providers describe "$PROVIDER_NAME" \
  --workload-identity-pool="$POOL_NAME" \
  --location="global" \
  --project="$PROJECT_ID" &>/dev/null; then
  info "Provider already exists, skipping..."
else
  gcloud iam workload-identity-pools providers create-oidc "$PROVIDER_NAME" \
    --workload-identity-pool="$POOL_NAME" \
    --location="global" \
    --issuer-uri="https://token.actions.githubusercontent.com" \
    --attribute-mapping="google.subject=assertion.sub,attribute.repository=assertion.repository,attribute.actor=assertion.actor" \
    --attribute-condition="assertion.repository=='${GITHUB_REPO}'" \
    --project="$PROJECT_ID"
  success "Workload Identity Provider created"
fi

# サービスアカウントへの Workload Identity User ロールの付与
info "Binding Workload Identity User role..."
gcloud iam service-accounts add-iam-policy-binding "$SA_EMAIL" \
  --role="roles/iam.workloadIdentityUser" \
  --member="principalSet://iam.googleapis.com/projects/$(gcloud projects describe $PROJECT_ID --format='value(projectNumber)')/locations/global/workloadIdentityPools/${POOL_NAME}/attribute.repository/${GITHUB_REPO}" \
  --project="$PROJECT_ID" \
  --quiet
success "Workload Identity binding complete"

# GitHub Secrets に登録する情報を出力
info ""
success "=== WIF Setup Complete ==="
info ""
info "GitHub Secrets に以下の情報を登録してください:"
info ""
echo "GCP_PROJECT_ID: $PROJECT_ID"
echo "GCP_REGION: $REGION"
echo "GCP_SERVICE_NAME: $SERVICE_NAME"
echo "GCP_WIF_PROVIDER: projects/$(gcloud projects describe $PROJECT_ID --format='value(projectNumber)')/locations/global/workloadIdentityPools/${POOL_NAME}/providers/${PROVIDER_NAME}"
echo "GCP_SERVICE_ACCOUNT: $SA_EMAIL"
info ""
info "コマンド例:"
info "  gh secret set GCP_PROJECT_ID --body \"$PROJECT_ID\""
info "  gh secret set GCP_REGION --body \"$REGION\""
info "  gh secret set GCP_SERVICE_NAME --body \"$SERVICE_NAME\""
info "  gh secret set GCP_WIF_PROVIDER --body \"projects/$(gcloud projects describe $PROJECT_ID --format='value(projectNumber)')/locations/global/workloadIdentityPools/${POOL_NAME}/providers/${PROVIDER_NAME}\""
info "  gh secret set GCP_SERVICE_ACCOUNT --body \"$SA_EMAIL\""
info ""
success "Setup script finished successfully!"
