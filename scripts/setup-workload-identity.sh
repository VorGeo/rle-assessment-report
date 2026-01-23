#!/bin/bash
# Setup Workload Identity Federation for GitHub Actions with Earth Engine
# This script configures keyless authentication for the rle-assessment-report repository

set -e  # Exit on error

# Configuration
PROJECT_ID="goog-rle-assessments"
POOL_NAME="github-actions"
PROVIDER_NAME="github-provider"
SERVICE_ACCOUNT_NAME="github-actions-ee"
REPO_OWNER="VorGeo"
REPO_NAME="rle-assessment-report"

echo "=================================================="
echo "Workload Identity Federation Setup"
echo "Project: ${PROJECT_ID}"
echo "Repository: ${REPO_OWNER}/${REPO_NAME}"
echo "=================================================="
echo ""

# Step 1: Authenticate and set project
echo "Step 1: Setting up gcloud configuration..."
gcloud config set project ${PROJECT_ID}

# Get project number
PROJECT_NUMBER=$(gcloud projects describe ${PROJECT_ID} --format="value(projectNumber)")
echo "Project Number: ${PROJECT_NUMBER}"
echo ""

# Step 2: Create Workload Identity Pool
echo "Step 2: Creating Workload Identity Pool..."
if gcloud iam workload-identity-pools describe ${POOL_NAME} \
    --project=${PROJECT_ID} \
    --location=global &>/dev/null; then
    echo "  ✓ Workload Identity Pool '${POOL_NAME}' already exists"
else
    gcloud iam workload-identity-pools create ${POOL_NAME} \
        --project=${PROJECT_ID} \
        --location=global \
        --display-name="GitHub Actions Pool"
    echo "  ✓ Created Workload Identity Pool"
fi
echo ""

# Step 3: Create Workload Identity Provider
echo "Step 3: Creating Workload Identity Provider..."
if gcloud iam workload-identity-pools providers describe ${PROVIDER_NAME} \
    --project=${PROJECT_ID} \
    --location=global \
    --workload-identity-pool=${POOL_NAME} &>/dev/null; then
    echo "  ✓ Workload Identity Provider '${PROVIDER_NAME}' already exists"
else
    gcloud iam workload-identity-pools providers create-oidc ${PROVIDER_NAME} \
        --project=${PROJECT_ID} \
        --location=global \
        --workload-identity-pool=${POOL_NAME} \
        --display-name="GitHub Provider" \
        --attribute-mapping="google.subject=assertion.sub,attribute.repository=assertion.repository,attribute.repository_owner=assertion.repository_owner" \
        --attribute-condition="assertion.repository_owner == '${REPO_OWNER}'" \
        --issuer-uri="https://token.actions.githubusercontent.com"
    echo "  ✓ Created Workload Identity Provider"
fi
echo ""

# Step 4: Create Service Account
echo "Step 4: Creating Service Account..."
SERVICE_ACCOUNT_EMAIL="${SERVICE_ACCOUNT_NAME}@${PROJECT_ID}.iam.gserviceaccount.com"

if gcloud iam service-accounts describe ${SERVICE_ACCOUNT_EMAIL} &>/dev/null; then
    echo "  ✓ Service Account already exists: ${SERVICE_ACCOUNT_EMAIL}"
else
    gcloud iam service-accounts create ${SERVICE_ACCOUNT_NAME} \
        --display-name="GitHub Actions Earth Engine" \
        --project=${PROJECT_ID}
    echo "  ✓ Created Service Account: ${SERVICE_ACCOUNT_EMAIL}"
fi
echo ""

# Step 5: Grant Earth Engine Permissions
echo "Step 5: Granting Earth Engine permissions..."
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
    --member="serviceAccount:${SERVICE_ACCOUNT_EMAIL}" \
    --role="roles/earthengine.writer" \
    --condition=None \
    --quiet
echo "  ✓ Granted Earth Engine Writer role"
echo ""

# Step 6: Allow GitHub Actions to impersonate the Service Account
echo "Step 6: Configuring Workload Identity binding..."
WORKLOAD_IDENTITY_MEMBER="principalSet://iam.googleapis.com/projects/${PROJECT_NUMBER}/locations/global/workloadIdentityPools/${POOL_NAME}/attribute.repository/${REPO_OWNER}/${REPO_NAME}"

gcloud iam service-accounts add-iam-policy-binding ${SERVICE_ACCOUNT_EMAIL} \
    --project=${PROJECT_ID} \
    --role="roles/iam.workloadIdentityUser" \
    --member="${WORKLOAD_IDENTITY_MEMBER}" \
    --quiet
echo "  ✓ Configured workload identity binding"
echo ""

# Step 7: Get Workload Identity Provider resource name
echo "Step 7: Getting configuration values..."
PROVIDER_RESOURCE_NAME=$(gcloud iam workload-identity-pools providers describe ${PROVIDER_NAME} \
    --project=${PROJECT_ID} \
    --location=global \
    --workload-identity-pool=${POOL_NAME} \
    --format="value(name)")

echo ""
echo "=================================================="
echo "✓ Setup Complete!"
echo "=================================================="
echo ""
echo "Next Steps:"
echo ""
echo "1. Add the following secrets to GitHub:"
echo "   Go to: https://github.com/${REPO_OWNER}/${REPO_NAME}/settings/secrets/actions"
echo ""
echo "   Secret 1:"
echo "   Name:  GCP_WORKLOAD_IDENTITY_PROVIDER"
echo "   Value: ${PROVIDER_RESOURCE_NAME}"
echo ""
echo "   Secret 2:"
echo "   Name:  GCP_SERVICE_ACCOUNT"
echo "   Value: ${SERVICE_ACCOUNT_EMAIL}"
echo ""
echo "2. The GitHub Actions workflow file will be updated automatically."
echo ""
echo "=================================================="
echo ""

# Save configuration to a file for reference
cat > workload-identity-config.txt <<EOF
Workload Identity Federation Configuration
===========================================

Project ID: ${PROJECT_ID}
Project Number: ${PROJECT_NUMBER}
Service Account Email: ${SERVICE_ACCOUNT_EMAIL}

GitHub Secrets to Add:
----------------------

GCP_WORKLOAD_IDENTITY_PROVIDER:
${PROVIDER_RESOURCE_NAME}

GCP_SERVICE_ACCOUNT:
${SERVICE_ACCOUNT_EMAIL}

Repository: ${REPO_OWNER}/${REPO_NAME}
EOF

echo "Configuration saved to: workload-identity-config.txt"
echo ""
