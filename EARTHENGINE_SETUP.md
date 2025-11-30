# Earth Engine Authentication Setup for GitHub Actions

This document explains how to configure Workload Identity Federation for Earth Engine authentication in GitHub Actions.

## Overview

The project uses **Workload Identity Federation** to authenticate with Google Earth Engine in CI/CD workflows. This approach is more secure than using service account keys because:

- No long-lived credentials are stored in GitHub
- Short-lived tokens are generated on-demand
- Fine-grained access control via IAM
- Google's recommended best practice

## Prerequisites

- Access to the `goog-rle-assessments` Google Cloud project
- Permissions to create service accounts and configure Workload Identity
- GitHub repository admin access to add secrets

## Setup Instructions

### 1. Create a Service Account

```bash
# Set your GCP project
export PROJECT_ID="goog-rle-assessments"

# Create a service account for GitHub Actions
gcloud iam service-accounts create github-actions-ee \
  --display-name="GitHub Actions Earth Engine" \
  --project=$PROJECT_ID
```

### 2. Grant Earth Engine Permissions

```bash
# Get the service account email
export SA_EMAIL="github-actions-ee@${PROJECT_ID}.iam.gserviceaccount.com"

# Grant Earth Engine API access
# Note: You may need to grant specific Earth Engine roles or permissions
# depending on your organization's setup
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:${SA_EMAIL}" \
  --role="roles/earthengine.viewer"

# If you need write access for EE assets:
# gcloud projects add-iam-policy-binding $PROJECT_ID \
#   --member="serviceAccount:${SA_EMAIL}" \
#   --role="roles/earthengine.writer"
```

### 3. Create Workload Identity Pool

```bash
# Create a Workload Identity Pool
gcloud iam workload-identity-pools create "github-actions-pool" \
  --location="global" \
  --display-name="GitHub Actions Pool" \
  --project=$PROJECT_ID

# Create a Workload Identity Provider for GitHub
gcloud iam workload-identity-pools providers create-oidc "github-provider" \
  --location="global" \
  --workload-identity-pool="github-actions-pool" \
  --display-name="GitHub Provider" \
  --attribute-mapping="google.subject=assertion.sub,attribute.actor=assertion.actor,attribute.repository=assertion.repository,attribute.repository_owner=assertion.repository_owner" \
  --attribute-condition="assertion.repository_owner == 'VorGeo'" \
  --issuer-uri="https://token.actions.githubusercontent.com" \
  --project=$PROJECT_ID
```

### 4. Allow GitHub to Impersonate the Service Account

```bash
# Get the project number
export PROJECT_NUMBER=$(gcloud projects describe $PROJECT_ID --format="value(projectNumber)")

# Allow the specific GitHub repository to impersonate the service account
gcloud iam service-accounts add-iam-policy-binding "${SA_EMAIL}" \
  --role="roles/iam.workloadIdentityUser" \
  --member="principalSet://iam.googleapis.com/projects/${PROJECT_NUMBER}/locations/global/workloadIdentityPools/github-actions-pool/attribute.repository/VorGeo/rle-assessment-report" \
  --project=$PROJECT_ID
```

### 5. Get the Workload Identity Provider Resource Name

```bash
# Get the full provider resource name
gcloud iam workload-identity-pools providers describe "github-provider" \
  --location="global" \
  --workload-identity-pool="github-actions-pool" \
  --project=$PROJECT_ID \
  --format="value(name)"
```

This will output something like:
```
projects/123456789/locations/global/workloadIdentityPools/github-actions-pool/providers/github-provider
```

### 6. Configure GitHub Secrets

Add the following secrets to your GitHub repository (Settings → Secrets and variables → Actions → New repository secret):

1. **`WIF_PROVIDER`**
   - Value: The full Workload Identity Provider resource name from step 5
   - Example: `projects/123456789/locations/global/workloadIdentityPools/github-actions-pool/providers/github-provider`

2. **`WIF_SERVICE_ACCOUNT`**
   - Value: The service account email
   - Example: `github-actions-ee@goog-rle-assessments.iam.gserviceaccount.com`

## How It Works

Once configured, the authentication flow is automatic:

1. The `google-github-actions/auth@v2` action authenticates with GCP using Workload Identity Federation
2. It sets the `GOOGLE_APPLICATION_CREDENTIALS` environment variable to point to temporary service account credentials
3. When your Python code calls `google.auth.default()`, it loads these Application Default Credentials (ADC)
4. The credentials are then passed to `ee.Initialize(credentials=credentials, project='goog-rle-assessments')`
5. **No separate `earthengine authenticate` command is needed** - the credentials are already available

This is why the workflow does NOT include an explicit "Authenticate Earth Engine" step. The Earth Engine Python library uses the credentials set up by the GCP auth action through `google.auth.default()`.

### Python Code Pattern

The code uses this pattern to initialize Earth Engine with ADC:

```python
import ee
from google.auth import default

# Load Application Default Credentials
credentials, _ = default(scopes=[
    'https://www.googleapis.com/auth/earthengine',
    'https://www.googleapis.com/auth/cloud-platform'
])

# Initialize Earth Engine with the credentials
ee.Initialize(credentials=credentials, project='goog-rle-assessments')
```

This works both locally (after running `gcloud auth application-default login`) and in CI/CD (with Workload Identity Federation).

## Verification

To verify the setup works:

1. Push a commit to the `main` branch or trigger the workflow manually
2. Check the GitHub Actions run log
3. The "Authenticate to Google Cloud" step should succeed and show credential file creation
4. The "Render Quarto Project" step should be able to access Earth Engine without additional authentication

## Troubleshooting

### "Failed to generate Google Cloud access token"

- Verify the `WIF_PROVIDER` secret contains the full resource name
- Check that the Workload Identity Pool and Provider exist
- Ensure the attribute condition matches your repository owner (`VorGeo`)

### "Permission denied" errors

- Verify the service account has the necessary Earth Engine roles
- Check that the IAM policy binding was created correctly
- Ensure the service account is enabled

### "Authentication failed" or permission errors when accessing Earth Engine

- Check that the Google Cloud authentication step completed successfully
- Verify the service account has the necessary Earth Engine roles (e.g., `roles/earthengine.viewer`)
- Ensure the service account has been registered with Earth Engine (may require admin approval)
- Check that `GOOGLE_APPLICATION_CREDENTIALS` environment variable is set in the workflow logs
- Verify the `ee.Initialize(project='goog-rle-assessments')` call uses the correct project ID

## Security Considerations

- The Workload Identity Federation is configured to only allow authentication from the `VorGeo` organization
- To restrict further, update the `--attribute-condition` to specify the exact repository
- Regularly audit service account permissions
- Use least-privilege IAM roles

## References

- [Google Cloud Workload Identity Federation](https://cloud.google.com/iam/docs/workload-identity-federation)
- [GitHub Actions OIDC](https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/about-security-hardening-with-openid-connect)
- [google-github-actions/auth](https://github.com/google-github-actions/auth)
- [Earth Engine Authentication](https://developers.google.com/earth-engine/guides/auth)
